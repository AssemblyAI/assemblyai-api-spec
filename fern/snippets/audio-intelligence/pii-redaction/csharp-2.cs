var data = new
{
    audio_url = audioUrl,
    redact_pii = true,
    redact_pii_policies = new[] { "person_name", "organization", "occupation" },
    redact_pii_sub = "hash",
    redact_pii_audio = true,
    redact_pii_audio_quality = "wav" // Optional. Defaults to "mp3"
};

// ...
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

          // Wait for the redacted audio
          string redactedAudioUrl = await WaitForRedactedAudioAsync(transcript.Id, httpClient, baseUrl);
      }
  }

// ...

static async Task<string> WaitForRedactedAudioAsync(string transcriptId, HttpClient httpClient, string baseUrl)
{
    string redactedAudioPollingEndpoint = $"{baseUrl}/v2/transcript/{transcriptId}/redacted-audio";

    while (true)
    {
        var pollingResponse = await httpClient.GetAsync(redactedAudioPollingEndpoint);
        var responseContent = await pollingResponse.Content.ReadAsStringAsync();

        var redactedAudioResult = JsonSerializer.Deserialize<RedactedAudioResult>(
            responseContent,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true }
        );

        if (redactedAudioResult.Status == "redacted_audio_ready")
        {
            Console.WriteLine(redactedAudioResult.RedactedAudioUrl);
            return redactedAudioResult.RedactedAudioUrl;
        }
        else if (redactedAudioResult.Status == "error")
        {
            throw new Exception($"Redacted audio failed: {redactedAudioResult.Error}");
        }
        else
        {
            await Task.Delay(TimeSpan.FromSeconds(3));
        }
    }
}

// ...

public class RedactedAudioResult
{
    [JsonPropertyName("status")]
    public string Status { get; set; }

    [JsonPropertyName("redacted_audio_url")]
    public string RedactedAudioUrl { get; set; }

    [JsonPropertyName("error")]
    public string Error { get; set; }
}
