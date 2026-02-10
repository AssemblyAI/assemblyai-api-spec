using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Text.Json.Serialization;
using System.Collections.Generic;

class Program
{
    static async Task Main(string[] args)
    {
        string baseUrl = "https://api.assemblyai.com";

        using (var httpClient = new HttpClient())
        {
            httpClient.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("<YOUR_API_KEY>");

            string uploadUrl = await UploadFileAsync("./local_file.mp3", httpClient, baseUrl);

            var transcript = await CreateTranscriptWithPiiRedactionAsync(uploadUrl, httpClient, baseUrl);

            Console.WriteLine($"Transcript ID: {transcript.Id}");
            transcript = await WaitForTranscriptToProcessAndGetRedactedText(transcript, httpClient, baseUrl);
        }
    }

    static async Task<string> UploadFileAsync(string filePath, HttpClient httpClient, string baseUrl)
    {
        using (var fileStream = File.OpenRead(filePath))
        using (var fileContent = new StreamContent(fileStream))
        {
            fileContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");

            using (var response = await httpClient.PostAsync($"{baseUrl}/v2/upload", fileContent))
            {
                response.EnsureSuccessStatusCode();
                var jsonDoc = await response.Content.ReadFromJsonAsync<JsonDocument>();
                return jsonDoc.RootElement.GetProperty("upload_url").GetString();
            }
        }
    }

    static async Task<Transcript> CreateTranscriptWithPiiRedactionAsync(string audioUrl, HttpClient httpClient, string baseUrl)
    {
        var data = new
        {
            audio_url = audioUrl,
            speech_models = new[] { "universal-3-pro", "universal-2" },
            language_detection = true,
            redact_pii = true,
            redact_pii_policies = new[] { "person_name", "organization", "occupation" },
            redact_pii_sub = "hash"
        };

        var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

        using (var response = await httpClient.PostAsync($"{baseUrl}/v2/transcript", content))
        {
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<Transcript>();
        }
    }

    static async Task<Transcript> WaitForTranscriptToProcessAndGetRedactedText(Transcript transcript, HttpClient httpClient, string baseUrl)
    {
        string pollingEndpoint = $"{baseUrl}/v2/transcript/{transcript.Id}";

        while (true)
        {
            var pollingResponse = await httpClient.GetAsync(pollingEndpoint);
            transcript = await pollingResponse.Content.ReadFromJsonAsync<Transcript>();

            switch (transcript.Status)
            {
                case "completed":
                    // Print the redacted transcript text
                    Console.WriteLine(transcript.Text);
                    return transcript;

                case "error":
                    throw new Exception($"Transcription failed: {transcript.Error}");

                default:
                    await Task.Delay(TimeSpan.FromSeconds(3));
                    break;
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

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }
}
