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

            var transcript = await CreateTranscriptWithAutoChaptersAsync(uploadUrl, httpClient, baseUrl);

            Console.WriteLine($"Transcript ID: {transcript.Id}");
            transcript = await WaitForTranscriptToProcessAndGetChapters(transcript, httpClient, baseUrl);
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

    static async Task<Transcript> CreateTranscriptWithAutoChaptersAsync(string audioUrl, HttpClient httpClient, string baseUrl)
    {
        var data = new
        {
            audio_url = audioUrl,
            speech_models = new[] { "universal-3-pro", "universal-2" },
            language_detection = true,
            auto_chapters = true
        };

        var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

        using (var response = await httpClient.PostAsync($"{baseUrl}/v2/transcript", content))
        {
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<Transcript>();
        }
    }

    static async Task<Transcript> WaitForTranscriptToProcessAndGetChapters(Transcript transcript, HttpClient httpClient, string baseUrl)
    {
        string pollingEndpoint = $"{baseUrl}/v2/transcript/{transcript.Id}";

        while (true)
        {
            var pollingResponse = await httpClient.GetAsync(pollingEndpoint);
            transcript = await pollingResponse.Content.ReadFromJsonAsync<Transcript>();

            switch (transcript.Status)
            {
                case "completed":
                    // Process auto chapters results
                    if (transcript.Chapters != null)
                    {
                        foreach (var chapter in transcript.Chapters)
                        {
                            Console.WriteLine($"{chapter.Start} - {chapter.End}: {chapter.Headline}");
                        }
                    }

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

        [JsonPropertyName("chapters")]
        public List<Chapter> Chapters { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }

    public class Chapter
    {
        [JsonPropertyName("start")]
        public int Start { get; set; }

        [JsonPropertyName("end")]
        public int End { get; set; }

        [JsonPropertyName("headline")]
        public string Headline { get; set; }
    }
}
