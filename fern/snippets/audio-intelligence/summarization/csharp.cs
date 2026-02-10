using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Text.Json.Serialization;

class Program
{
    static async Task Main(string[] args)
    {
        using (var httpClient = new HttpClient())
        {
            httpClient.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("<YOUR_API_KEY>");

            var uploadUrl = await UploadFileAsync("./my-audio.mp3", httpClient);

            var transcript = await CreateTranscriptAsync(uploadUrl, httpClient);

            transcript = await WaitForTranscriptToProcess(transcript, httpClient);

            // Print the transcript ID and summary
            Console.WriteLine($"Transcript ID: {transcript.Id}");
            Console.WriteLine(transcript.Summary);
        }
    }

    static async Task<string> UploadFileAsync(string filePath, HttpClient httpClient)
    {
        using (var fileStream = File.OpenRead(filePath))
        using (var fileContent = new StreamContent(fileStream))
        {
            fileContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");

            using (var response = await httpClient.PostAsync("https://api.assemblyai.com/v2/upload", fileContent))
            {
                response.EnsureSuccessStatusCode();
                var jsonDoc = await response.Content.ReadFromJsonAsync<JsonDocument>();
                return jsonDoc.RootElement.GetProperty("upload_url").GetString();
            }
        }
    }

    static async Task<Transcript> CreateTranscriptAsync(string audioUrl, HttpClient httpClient)
    {
        var data = new {
            audio_url = audioUrl,
            speech_models = new[] { "universal-3-pro", "universal-2" },
            language_detection = true,
            summarization = true,
            summary_model = "informative",
            summary_type = "bullets"
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

            if (transcript.Status == "completed")
            {
                return transcript;
            }
            else if (transcript.Status == "error")
            {
                throw new Exception($"Transcription failed: {transcript.Error}");
            }
            else
            {
                await Task.Delay(TimeSpan.FromSeconds(3));
            }
        }
    }

    public class Transcript
    {
        [JsonPropertyName("id")]
        public string Id { get; set; }

        [JsonPropertyName("status")]
        public string Status { get; set; }

        [JsonPropertyName("text")]
        public string Text { get; set; }

        [JsonPropertyName("summary")]
        public string Summary { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }
}
