using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

public class Transcript
{
    public string Id { get; set; }
    public string Status { get; set; }
    public string Text { get; set; }
    public string Error { get; set; }
}

class Program
{
    static void Main(string[] args)
    {
        MainAsync(args).GetAwaiter().GetResult();
    }

    static async Task MainAsync(string[] args)
    {
        using (var httpClient = new HttpClient())
        {
            httpClient.DefaultRequestHeaders.Add("authorization", "<YOUR-API-KEY>");

            var uploadUrl = await UploadFileAsync("audio.mp3", httpClient);
            var transcript = await CreateTranscriptAsync(uploadUrl, httpClient);
            transcript = await WaitForTranscriptToProcess(transcript, httpClient);

            Console.WriteLine(transcript.Text);

            var deleteResponse = await DeleteTranscriptAsync(transcript.Id, httpClient);
            Console.WriteLine(deleteResponse.RootElement.GetProperty("text").GetString());
        }
    }

    static async Task<string> UploadFileAsync(string filePath, HttpClient httpClient)
    {
        using (var fileStream = File.OpenRead(filePath))
        using (var fileContent = new StreamContent(fileStream))
        {
            fileContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");

            var response = await httpClient.PostAsync("https://api.assemblyai.com/v2/upload", fileContent);
            response.EnsureSuccessStatusCode();

            var jsonDoc = await response.Content.ReadFromJsonAsync<JsonDocument>();
            return jsonDoc.RootElement.GetProperty("upload_url").GetString();
        }
    }

    static async Task<Transcript> CreateTranscriptAsync(string audioUrl, HttpClient httpClient)
    {
        var data = new
        {
            audio_url = audioUrl,
            speech_models = new[] { "universal-3-pro", "universal-2" },
            language_detection = true
        };
        var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

        using (var response = await httpClient.PostAsync("https://api.assemblyai.com/v2/transcript", content))
        {
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<Transcript>();
        }
    }

    static async Task<Transcript> WaitForTranscriptToProcess(Transcript transcript, HttpClient httpClient)
    {
        var pollingEndpoint = $"https://api.assemblyai.com/v2/transcript/{transcript.Id}";

        while (true)
        {
            var pollingResponse = await httpClient.GetAsync(pollingEndpoint);
            transcript = await pollingResponse.Content.ReadFromJsonAsync<Transcript>();

            switch (transcript.Status)
            {
                case "queued":
                case "processing":
                    await Task.Delay(TimeSpan.FromSeconds(3));
                    break;
                case "completed":
                    return transcript;
                case "error":
                    throw new Exception($"Transcription failed: {transcript.Error}");
                default:
                    throw new Exception("Unexpected transcript status.");
            }
        }
    }

    static async Task<JsonDocument> DeleteTranscriptAsync(string transcriptId, HttpClient httpClient)
    {
        var url = $"https://api.assemblyai.com/v2/transcript/{transcriptId}";
        var response = await httpClient.DeleteAsync(url);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<JsonDocument>();
    }
}
