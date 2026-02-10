import axios from "axios";

// Step 1: Transcribe an audio file.
const base_url = "https://api.assemblyai.com";

const headers = {
authorization: "<YOUR_API_KEY>",
};

// import fs from 'fs-extra';
// const path = './my-audio.mp3';
// const audioData = await fs.readFile(path)
// const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, {
// headers
// })
// const uploadUrl = uploadResponse.data.upload_url

// Or use a publicly-accessibly URL:
const uploadUrl = "https://assembly.ai/sports_injuries.mp3";

const data = {
audio_url: uploadUrl,
};

const response = await axios.post(base_url + "/v2/transcript", data, {
headers,
});

const transcript_id = response.data.id;
const polling_endpoint = base_url + `/v2/transcript/${transcript_id}`;

let transcript;
while (true) {
transcript = (await axios.get(polling_endpoint, { headers })).data;

if (transcript.status === "completed") {
break;
} else if (transcript.status === "error") {
throw new Error(`Transcription failed: ${transcript.error}`);
} else {
await new Promise((resolve) => setTimeout(resolve, 3000));
}
}

// Step 2: Define a prompt with your question(s).
const prompt = "What is a runner's knee?";

// Step 3: Send to LLM Gateway.
const llm_gateway_data = {
model: "claude-sonnet-4-5-20250929",
messages: [
{ role: "user", content: `${prompt}\n\nTranscript: ${transcript.text}` }
],
max_tokens: 1000
};

const result = await axios.post(
"https://llm-gateway.assemblyai.com/v1/chat/completions",
llm_gateway_data,
{ headers }
);
console.log(result.data.choices[0].message.content);

````
</Tab>

<Tab language="csharp" title="C#">

```csharp {122-123,125-127}
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

   // Step 1: Transcribe an audio file.
   // var uploadUrl = await UploadFileAsync("/my_audio.mp3", httpClient);
   // Or use a publicly-accessible URL.
   var uploadUrl = "https://assembly.ai/sports_injuries.mp3";
   var transcript = await CreateTranscriptAsync(uploadUrl, httpClient);
   transcript = await WaitForTranscriptToProcess(transcript, httpClient);

   // Step 2: Define a prompt with your question(s).
   const string prompt = "What is a runner's knee?";

   // Step 3: Send to LLM Gateway.
   var llmGatewayResponse = await SendToLlmGatewayAsync(prompt, transcript.Text, httpClient);

   Console.WriteLine(llmGatewayResponse.Choices[0].Message.Content);
}
````

</Tab>
<Tab language="ruby" title="Ruby">

```ruby {47-48,50-59}
require 'net/http'
require 'json'

# Step 1: Transcribe an audio file.
base_url = "https://api.assemblyai.com"
headers = {
   "authorization" => "<YOUR_API_KEY>",
   "content-type" => "application/json"
}

# path = "/my_audio.mp3"
# uri = URI("#{base_url}/v2/upload")
# request = Net::HTTP::Post.new(uri, headers)
# request.body = File.read(path)

# http = Net::HTTP.new(uri.host, uri.port)
# http.use_ssl = true
# upload_response = http.request(request)
# upload_url = JSON.parse(upload_response.body)["upload_url"]

# Or use a publicly-accessible URL:
upload_url = "https://assembly.ai/sports_injuries.mp3"

uri = URI("#{base_url}/v2/transcript")
request = Net::HTTP::Post.new(uri, headers)
request.body = { audio_url: upload_url }.to_json

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
response = http.request(request)
transcript_id = JSON.parse(response.body)["id"]
polling_endpoint = "#{base_url}/v2/transcript/#{transcript_id}"

while true
   polling_uri = URI(polling_endpoint)
   polling_request = Net::HTTP::Get.new(polling_uri, headers)
   polling_response = http.request(polling_request)
   transcription_result = JSON.parse(polling_response.body)

   if transcription_result["status"] == "completed"
       break
   elsif transcription_result["status"] == "error"
       raise "Transcription failed: #{transcription_result["error"]}"
   else
       sleep(3)
   end
end

# Step 2: Define a prompt with your question(s).
prompt = "What is a runner's knee?"

# Step 3: Send to LLM Gateway.
llm_gateway_uri = URI("https://llm-gateway.assemblyai.com/v1/chat/completions")
llm_gateway_request = Net::HTTP::Post.new(llm_gateway_uri, headers)
llm_gateway_request.body = {
  model: "claude-sonnet-4-5-20250929",
  messages: [
    { role: "user", content: "#{prompt}\n\nTranscript: #{transcription_result['text']}" }
  ],
  max_tokens: 1000
}.to_json

llm_gateway_http = Net::HTTP.new(llm_gateway_uri.host, llm_gateway_uri.port)
llm_gateway_http.use_ssl = true
llm_gateway_response = llm_gateway_http.request(llm_gateway_request)
llm_gateway_result = JSON.parse(llm_gateway_response.body)
puts llm_gateway_result["choices"][0]["message"]["content"]
