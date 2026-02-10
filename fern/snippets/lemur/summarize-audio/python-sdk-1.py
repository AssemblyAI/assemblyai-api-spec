import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Step 1: Transcribe an audio file.

# audio_file = "./local_file.mp3"

audio_file = "https://assembly.ai/sports_injuries.mp3"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_file)

# Step 2: Define a summarization prompt.

prompt = "Provide a brief summary of the transcript."

# Step 3: Apply LeMUR.

result = transcript.lemur.task(
prompt, final_model=aai.LemurModel.claude_sonnet_4_20250514
)

print(result.response)

````

</Tab>
<Tab language="python" title="Python">

```python {40-41,43-50}
import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
  "authorization": "<YOUR_API_KEY>"
}

# Step 1: Transcribe an audio file.
# with open("./my-audio.mp3", "rb") as f:
# response = requests.post(base_url + "/v2/upload",
#                         headers=headers,
#                         data=f)
# upload_url = response.json()["upload_url"]

upload_url = "https://assembly.ai/sports_injuries.mp3"

data = {
  "audio_url": upload_url
}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

while True:
  transcript = requests.get(polling_endpoint, headers=headers).json()

  if transcript["status"] == "completed":
    break

  elif transcript["status"] == "error":
    raise RuntimeError(f"Transcription failed: {transcript['error']}")

  else:
    time.sleep(3)

# Step 2: Define a summarization prompt.
prompt = "Provide a brief summary of the transcript."

# Step 3: Apply LeMUR.
lemur_data = {
  "prompt": prompt,
  "transcript_ids": [transcript_id],
  "final_model": "anthropic/claude-sonnet-4-20250514",
}

result = requests.post(base_url + "/lemur/v3/generate/task", headers=headers, json=lemur_data)

print(result.json()["response"])
````

</Tab>
<Tab language="javascript-sdk" title="JavaScript SDK">
  
```javascript {13-14,16-21}
import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
apiKey: "<YOUR_API_KEY>",
});

const run = async () => {
// Step 1: Transcribe an audio file.
//const audioFile = './local_file.mp3'
const audioFile = "https://assembly.ai/sports_injuries.mp3";
const transcript = await client.transcripts.transcribe({ audio: audioFile });

// Step 2: Define a summarization prompt.
const prompt = "Provide a brief summary of the transcript.";

// Step 3: Apply LeMUR.
const { response } = await client.lemur.task({
transcript_ids: [transcript.id],
prompt,
final_model: "anthropic/claude-sonnet-4-20250514",
});

console.log(response);
};

run();

````

</Tab>
<Tab language="javascript" title="JavaScript">

```javascript {40-41,43-50}
import axios from "axios";
import fs from "fs-extra";

const base_url = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

// Step 1: Transcribe an audio file.
const path = "./my-audio.mp3";
const audioData = await fs.readFile(path);
const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, {
  headers,
});
const uploadUrl = uploadResponse.data.upload_url;

const data = {
  audio_url: uploadUrl, // You can also use a URL of an audio or video file on the web
};

const response = await axios.post(base_url + "/v2/transcript", data, {
  headers,
});

const transcript_id = response.data.id;
const polling_endpoint = base_url + `/v2/transcript/${transcript_id}`;

while (true) {
  const transcript = (await axios.get(polling_endpoint, { headers })).data;

  if (transcript.status === "completed") {
    break;
  } else if (transcript.status === "error") {
    throw new Error(`Transcription failed: ${transcript.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}

// Step 2: Define a summarization prompt.
const prompt = "Provide a brief summary of the transcript.";

// Step 3: Apply LeMUR.
const lemur_data = {
  prompt: prompt,
  transcript_ids: [transcript_id],
  final_model: "anthropic/claude-sonnet-4-20250514",
};

const result = await axios.post(
  base_url + "/lemur/v3/generate/task",
  lemur_data,
  { headers }
);

console.log(result.data.response);
````

</Tab>
<Tab language="csharp" title="C#">
  
```csharp {120-121,123-125}
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
var uploadUrl = await UploadFileAsync("/my_audio.mp3", httpClient);
var transcript = await CreateTranscriptAsync(uploadUrl, httpClient); // You can also replace uploadUrl with an audio file URL
transcript = await WaitForTranscriptToProcess(transcript, httpClient);

// Step 2: Define a summarization prompt.
const string prompt = "Provide a brief summary of the transcript.";

//Step 3: Apply LeMUR.
var transcriptIds = new List<string> { transcript.Id };
var lemurResponse = await GenerateTaskAsync(prompt, transcriptIds, httpClient);

Console.WriteLine(lemurResponse.Response);
}

````

</Tab>
<Tab language="ruby" title="Ruby">

```ruby {44-45,47-56}
require 'net/http'
require 'json'

base_url = "https://api.assemblyai.com"
headers = {
   "authorization" => "<YOUR_API_KEY>",
   "content-type" => "application/json"
}

# Step 1: Transcribe an audio file.
path = "/my_audio.mp3"
uri = URI("#{base_url}/v2/upload")
request = Net::HTTP::Post.new(uri, headers)
request.body = File.read(path)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
upload_response = http.request(request)
upload_url = JSON.parse(upload_response.body)["upload_url"]

uri = URI("#{base_url}/v2/transcript")
request = Net::HTTP::Post.new(uri, headers)
request.body = { audio_url: upload_url }.to_json # You can also replace upload_url with an audio file URL

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

# Step 2: Define a summarization prompt.
prompt = "Provide a brief summary of the transcript."

# Step 3: Apply LeMUR.
lemur_uri = URI("#{base_url}/lemur/v3/generate/task")
lemur_request = Net::HTTP::Post.new(lemur_uri, headers)
lemur_request.body = {
  final_model: "anthropic/claude-sonnet-4-20250514",
  prompt: prompt,
  transcript_ids: [transcript_id]
}.to_json

lemur_response = http.request(lemur_request)

lemur_result = JSON.parse(lemur_response.body)
puts lemur_result["response"]
````

</Tab>
<Tab language="php" title="PHP">

```php {54-55,57-70}
<?php
$base_url = "https://api.assemblyai.com";
$headers = array(
    "authorization: <YOUR_API_KEY>",
    "content-type: application/json"
);
$path = "/my_audio.mp3";

// Step 1: Transcribe an audio file.
$ch = curl_init($base_url . "/v2/upload");
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => file_get_contents($path),
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_RETURNTRANSFER => true
]);

$response = curl_exec($ch);
$upload_url = json_decode($response, true)["upload_url"];
curl_close($ch);

$ch = curl_init($base_url . "/v2/transcript");
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode(["audio_url" => $upload_url]), // You can also replace upload_url with an audio file URL
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_RETURNTRANSFER => true
]);

$response = curl_exec($ch);
$transcript_id = json_decode($response, true)['id'];
curl_close($ch);

$polling_endpoint = $base_url . "/v2/transcript/" . $transcript_id;

while (true) {
    $ch = curl_init($polling_endpoint);
    curl_setopt_array($ch, [
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_RETURNTRANSFER => true
    ]);

    $transcription_result = json_decode(curl_exec($ch), true);
    curl_close($ch);

    if ($transcription_result['status'] === "completed") {
        break;
    } else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    }
    sleep(3);
}

// Step 2: Define a summarization prompt.
$prompt = 'Provide a brief summary of the transcript.'

// Step 3: Apply LeMUR.
$ch = curl_init($base_url . "/lemur/v3/generate/task");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_POSTFIELDS => json_encode([
        'final_model' => 'anthropic/claude-sonnet-4-20250514',
        'prompt' => $prompt,
        'transcript_ids' => [$transcript_id]
    ])
]);

$response = curl_exec($ch);
$result = json_decode($response, true);
echo $result['response'];
curl_close($ch);
