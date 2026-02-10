using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class Transcript
{
   public string Id { get; set; }
   public string Status { get; set; }
   public string Text { get; set; }

   [JsonPropertyName("language_code")]
   public string LanguageCode { get; set; }

   public string Error { get; set; }
}

public class LemurResponse
{
  [JsonPropertyName("request_id")]
  public string RequestId { get; set; }

  public string Response { get; set; }

  public Usage Usage { get; set; }
}

public class Usage
{
  [JsonPropertyName("input_tokens")]
  public int InputTokens { get; set; }

  [JsonPropertyName("output_tokens")]
  public int OutputTokens { get; set; }
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

private static async Task<LemurResponse> GenerateTaskAsync(string prompt, List<string> transcriptIds, HttpClient httpClient)
{
   var data = new
   {
       transcript_ids = transcriptIds,
       prompt,
       final_model = "anthropic/claude-sonnet-4-20250514"
   };

   var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

   using var response = await httpClient.PostAsync("https://api.assemblyai.com/lemur/v3/generate/task", content);
   response.EnsureSuccessStatusCode();
   return await response.Content.ReadFromJsonAsync<LemurResponse>();
}

using (var httpClient = new HttpClient())
{
   httpClient.DefaultRequestHeaders.Authorization =
       new AuthenticationHeaderValue("<YOUR_API_KEY>");

   // Step 1: Transcribe an audio file.
   // var uploadUrl = await UploadFileAsync("/my_audio.mp3", httpClient);
   // Or use a publicly-accessible URL.
   var uploadUrl = "https://assembly.ai/call.mp4";
   var transcript = await CreateTranscriptAsync(uploadUrl, httpClient);
   transcript = await WaitForTranscriptToProcess(transcript, httpClient);

   // Step 2: Define your prompt.
   const string prompt = "What was the emotional sentiment of the phone call?";

   // Step 3: Apply LeMUR.
   var transcriptIds = new List<string> { transcript.Id };
   var lemurResponse = await GenerateTaskAsync(prompt, transcriptIds, httpClient);

   Console.WriteLine(lemurResponse.Response);
}
