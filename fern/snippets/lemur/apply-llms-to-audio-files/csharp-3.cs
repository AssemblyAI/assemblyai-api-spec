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

var llmGatewayResponse = await SendToLlmGatewayAsync(prompt, transcript.Text, httpClient);
