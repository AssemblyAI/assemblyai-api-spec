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

            var transcript = await CreateTranscriptWithContentSafetyAsync(uploadUrl, httpClient, baseUrl);

            Console.WriteLine($"Transcript ID: {transcript.Id}");
            transcript = await WaitForTranscriptToProcessAndAnalyzeContentSafety(transcript, httpClient, baseUrl);
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

    static async Task<Transcript> CreateTranscriptWithContentSafetyAsync(string audioUrl, HttpClient httpClient, string baseUrl)
    {
        var data = new
        {
            audio_url = audioUrl,
            speech_models = new[] { "universal-3-pro", "universal-2" },
            language_detection = true,
            content_safety = true
        };

        var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

        using (var response = await httpClient.PostAsync($"{baseUrl}/v2/transcript", content))
        {
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<Transcript>();
        }
    }

    static async Task<Transcript> WaitForTranscriptToProcessAndAnalyzeContentSafety(Transcript transcript, HttpClient httpClient, string baseUrl)
    {
        string pollingEndpoint = $"{baseUrl}/v2/transcript/{transcript.Id}";

        while (true)
        {
            var pollingResponse = await httpClient.GetAsync(pollingEndpoint);
            transcript = await pollingResponse.Content.ReadFromJsonAsync<Transcript>();

            switch (transcript.Status)
            {
                case "completed":
                    // Process content safety results
                    if (transcript.ContentSafetyLabels != null)
                    {
                        if (transcript.ContentSafetyLabels.Results != null)
                        {
                            foreach (var result in transcript.ContentSafetyLabels.Results)
                            {
                                Console.WriteLine(result.Text);
                                Console.WriteLine($"Timestamp: {result.Timestamp.Start} - {result.Timestamp.End}");

                                // Get category, confidence, and severity
                                foreach (var label in result.Labels)
                                {
                                    Console.WriteLine($"{label.LabelName} - {label.Confidence} - {label.Severity}");
                                }
                            }
                        }

                        // Get the confidence of the most common labels
                        if (transcript.ContentSafetyLabels.Summary != null)
                        {
                            foreach (var label in transcript.ContentSafetyLabels.Summary)
                            {
                                Console.WriteLine($"{label.Value * 100}% confident that the audio contains {label.Key}");
                            }
                        }

                        // Get the overall severity
                        if (transcript.ContentSafetyLabels.SeverityScoreSummary != null)
                        {
                            foreach (var label in transcript.ContentSafetyLabels.SeverityScoreSummary)
                            {
                                Console.WriteLine($"{label.Value.Low * 100}% confident that the audio contains low-severity {label.Key}");
                                Console.WriteLine($"{label.Value.Medium * 100}% confident that the audio contains medium-severity {label.Key}");
                                Console.WriteLine($"{label.Value.High * 100}% confident that the audio contains high-severity {label.Key}");
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

        [JsonPropertyName("content_safety_labels")]
        public ContentSafetyLabels ContentSafetyLabels { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }

    public class ContentSafetyLabels
    {
        [JsonPropertyName("status")]
        public string Status { get; set; }

        [JsonPropertyName("results")]
        public List<ContentSafetyResult> Results { get; set; }

        [JsonPropertyName("summary")]
        public Dictionary<string, double> Summary { get; set; }

        [JsonPropertyName("severity_score_summary")]
        public Dictionary<string, SeverityScore> SeverityScoreSummary { get; set; }
    }

    public class ContentSafetyResult
    {
        [JsonPropertyName("text")]
        public string Text { get; set; }

        [JsonPropertyName("timestamp")]
        public TimeRange Timestamp { get; set; }

        [JsonPropertyName("labels")]
        public List<Label> Labels { get; set; }

        [JsonPropertyName("sentences_idx_start")]
        public int SentencesIdxStart { get; set; }

        [JsonPropertyName("sentences_idx_end")]
        public int SentencesIdxEnd { get; set; }
    }

    public class TimeRange
    {
        [JsonPropertyName("start")]
        public int Start { get; set; }

        [JsonPropertyName("end")]
        public int End { get; set; }
    }

    public class Label
    {
        [JsonPropertyName("label")]
        public string LabelName { get; set; }

        [JsonPropertyName("confidence")]
        public double Confidence { get; set; }

        [JsonPropertyName("severity")]
        public double Severity { get; set; }
    }

    public class SeverityScore
    {
        [JsonPropertyName("low")]
        public double Low { get; set; }

        [JsonPropertyName("medium")]
        public double Medium { get; set; }

        [JsonPropertyName("high")]
        public double High { get; set; }
    }
}
