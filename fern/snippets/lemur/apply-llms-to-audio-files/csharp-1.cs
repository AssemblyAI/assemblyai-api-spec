using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

public class Transcript
{
 public string Id { get; set; }
 public string Status { get; set; }
 public string Text { get; set; }

 [JsonPropertyName("language_code")]
 public string LanguageCode { get; set; }

 public string Error { get; set; }
}

public class LlmGatewayResponse
{
 public List<Choice> Choices { get; set; }
}

public class Choice
{
 public Message Message { get; set; }
}

public class Message
{
 public string Content { get; set; }
}

private static async Task<string> UploadFileAsync(string filePath, HttpClient httpClient)
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

private static async Task<Transcript> CreateTranscriptAsync(string audioUrl, HttpClient httpClient)
{
 var data = new { audio_url = audioUrl };
 var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

 using (var response = await httpClient.PostAsync("https://api.assemblyai.com/v2/transcript", content))
 {
     response.EnsureSuccessStatusCode();
     return await response.Content.ReadFromJsonAsync<Transcript>();
 }
}

private static async Task<Transcript> WaitForTranscriptToProcess(Transcript transcript, HttpClient httpClient)
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
             await Task.Delay(TimeSpan.FromSeconds(3));
             break;
         case "completed":
             return transcript;
         case "error":
             throw new Exception($"Transcription failed: {transcript.Error}");
         default:
             throw new Exception("This code shouldn't be reachable.");
     }
 }
}

private static async Task<LlmGatewayResponse> SendToLlmGatewayAsync(string prompt, string transcriptText, HttpClient httpClient)
{
 var data = new
 {
     model = "claude-sonnet-4-5-20250929",
     messages = new[]
     {
         new { role = "user", content = $"{prompt}\n\nTranscript: {transcriptText}" }
     },
     max_tokens = 1000
 };

 var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

 using var response = await httpClient.PostAsync("https://llm-gateway.assemblyai.com/v1/chat/completions", content);
 response.EnsureSuccessStatusCode();
 return await response.Content.ReadFromJsonAsync<LlmGatewayResponse>();
}

using (var httpClient = new HttpClient())
{
 httpClient.DefaultRequestHeaders.Authorization =
     new AuthenticationHeaderValue("<YOUR_API_KEY>");

 const string prompt = "Provide a brief summary of the transcript.";

 // Step 1: Transcribe the audio
 var uploadUrl = await UploadFileAsync("/my_audio.mp3", httpClient);
 var transcript = await CreateTranscriptAsync(uploadUrl, httpClient); // You can also replace uploadUrl with an audio file URL
 transcript = await WaitForTranscriptToProcess(transcript, httpClient);

 // Step 2: Send transcript to LLM Gateway
 var llmGatewayResponse = await SendToLlmGatewayAsync(prompt, transcript.Text, httpClient);

 Console.WriteLine(llmGatewayResponse.Choices[0].Message.Content);
}
