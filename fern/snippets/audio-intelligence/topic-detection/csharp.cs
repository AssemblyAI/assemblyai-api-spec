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

            var transcript = await CreateTranscriptWithIabCategoriesAsync(uploadUrl, httpClient, baseUrl);

            Console.WriteLine($"Transcript ID: {transcript.Id}");
            transcript = await WaitForTranscriptToProcessAndAnalyzeCategories(transcript, httpClient, baseUrl);
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

    static async Task<Transcript> CreateTranscriptWithIabCategoriesAsync(string audioUrl, HttpClient httpClient, string baseUrl)
    {
        var data = new
        {
            audio_url = audioUrl,
            speech_models = new[] { "universal-3-pro", "universal-2" },
            language_detection = true,
            iab_categories = true
        };

        var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

        using (var response = await httpClient.PostAsync($"{baseUrl}/v2/transcript", content))
        {
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<Transcript>();
        }
    }

    static async Task<Transcript> WaitForTranscriptToProcessAndAnalyzeCategories(Transcript transcript, HttpClient httpClient, string baseUrl)
    {
        string pollingEndpoint = $"{baseUrl}/v2/transcript/{transcript.Id}";

        while (true)
        {
            var pollingResponse = await httpClient.GetAsync(pollingEndpoint);
            transcript = await pollingResponse.Content.ReadFromJsonAsync<Transcript>();

            switch (transcript.Status)
            {
                case "completed":
                    // Process IAB categories results
                    if (transcript.IabCategoriesResult != null)
                    {
                        // Get the parts of the transcript that were tagged with topics
                        if (transcript.IabCategoriesResult.Results != null)
                        {
                            foreach (var result in transcript.IabCategoriesResult.Results)
                            {
                                Console.WriteLine(result.Text);
                                Console.WriteLine($"Timestamp: {result.Timestamp.Start} - {result.Timestamp.End}");

                                foreach (var label in result.Labels)
                                {
                                    Console.WriteLine($"{label.Label} ({label.Relevance})");
                                }
                                Console.WriteLine();
                            }
                        }

                        // Get a summary of all topics in the transcript
                        if (transcript.IabCategoriesResult.Summary != null)
                        {
                            foreach (var topicEntry in transcript.IabCategoriesResult.Summary)
                            {
                                Console.WriteLine($"Audio is {topicEntry.Value * 100}% relevant to {topicEntry.Key}");
                            }
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

        [JsonPropertyName("iab_categories_result")]
        public IabCategoriesResult IabCategoriesResult { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }

    public class IabCategoriesResult
    {
        [JsonPropertyName("results")]
        public List<CategoryResult> Results { get; set; }

        [JsonPropertyName("summary")]
        public Dictionary<string, double> Summary { get; set; }
    }

    public class CategoryResult
    {
        [JsonPropertyName("text")]
        public string Text { get; set; }

        [JsonPropertyName("timestamp")]
        public TimeRange Timestamp { get; set; }

        [JsonPropertyName("labels")]
        public List<CategoryLabel> Labels { get; set; }
    }

    public class TimeRange
    {
        [JsonPropertyName("start")]
        public int Start { get; set; }

        [JsonPropertyName("end")]
        public int End { get; set; }
    }

    public class CategoryLabel
    {
        [JsonPropertyName("label")]
        public string Label { get; set; }

        [JsonPropertyName("relevance")]
        public double Relevance { get; set; }
    }
}
