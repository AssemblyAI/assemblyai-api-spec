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

            var localFilePath = "audio.mp3";

            Console.WriteLine("Uploading file...");
            var uploadUrl = await UploadFileAsync(localFilePath, httpClient);

            Console.WriteLine("Creating transcript with speech_model...");
            var transcript = await CreateTranscriptAsync(uploadUrl, httpClient);

            Console.WriteLine("Waiting for transcript...");
            transcript = await WaitForTranscriptToProcess(transcript, httpClient);

            Console.WriteLine("Transcription completed!");
            Console.WriteLine("----------------------------------");
            Console.WriteLine(transcript.Text);
        }
    }

    static async Task<string> UploadFileAsync(string filePath, HttpClient httpClient)
    {
        using (var fileStream = File.OpenRead(filePath))
        using (var content = new StreamContent(fileStream))
        {
            content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");

            var response = await httpClient.PostAsync("https://api.assemblyai.com/v2/upload", content);
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
            audio_start_from = 5000,
            audio_end_at = 15000
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
                case "processing":
                case "queued":
                    Console.WriteLine($"Status: {transcript.Status}... waiting...");
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
}
