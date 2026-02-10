import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
apiKey: "<YOUR_API_KEY>",
});

const audioUrl = "https://assembly.ai/meeting.mp4";

const run = async () => {
const transcript = await client.transcripts.transcribe({ audio: audioUrl });

const { response } = await client.lemur.summary({
transcript_ids: [transcript.id],
final_model: "anthropic/claude-sonnet-4-20250514",
context: "A GitLab meeting to discuss logistics",
answer_format: "TLDR",
});

console.log(response);
};

run();

````

</Tab>
<Tab language="javascript" title="JavaScript">

```javascript {33-40}
import axios from "axios";

const base_url = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

const uploadUrl = "https://assembly.ai/meeting.mp4";

const data = {
  audio_url: uploadUrl,
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

const lemur_data = {
  transcript_ids: [transcript_id],
  final_model: "anthropic/claude-sonnet-4-20250514",
  context: "A GitLab meeting to discuss logistics",
  answer_format: "TLDR",
};

const result = await axios.post(
  base_url + "/lemur/v3/generate/summary",
  lemur_data,
  { headers }
);

console.log(result.data.response);
````

</Tab>
<Tab language="csharp" title="C#">
  
```csharp {78-87, 105}
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

public class Program
{
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

    private static async Task<LemurResponse> GenerateSummaryAsync(List<string> transcriptIds, HttpClient httpClient)
    {
        var data = new
        {
            transcript_ids = transcriptIds,
            final_model = "anthropic/claude-sonnet-4-20250514",
            context = "A GitLab meeting to discuss logistics",
            answer_format = "TLDR"
        };
        var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

        using var response = await httpClient.PostAsync("https://api.assemblyai.com/lemur/v3/generate/summary", content);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<LemurResponse>();
    }

    public static async Task Main()
    {
        using (var httpClient = new HttpClient())
        {
            httpClient.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("<YOUR_API_KEY>");

            string audioUrl = "https://assembly.ai/meeting.mp4";

            var transcript = await CreateTranscriptAsync(audioUrl, httpClient);
            transcript = await WaitForTranscriptToProcess(transcript, httpClient);

            var transcriptIds = new List<string> { transcript.Id };
            var lemurResponse = await GenerateSummaryAsync(transcriptIds, httpClient);
            Console.WriteLine(lemurResponse.Response);
        }
    }

}

````

</Tab>
<Tab language="ruby" title="Ruby">

```ruby {35-45}
require 'net/http'
require 'json'

base_url = "https://api.assemblyai.com"
headers = {
   "authorization" => "<YOUR_API_KEY>",
   "content-type" => "application/json"
}

upload_url = "https://assembly.ai/meeting.mp4"

uri = URI("#{base_url}/v2/transcript")
request = Net::HTTP::Post.new(uri, headers)
request.body = { audio_url: upload_url }.to_json

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

lemur_uri = URI("#{base_url}/lemur/v3/generate/summary")
lemur_request = Net::HTTP::Post.new(lemur_uri, headers)
lemur_request.body = {
  final_model: "anthropic/claude-sonnet-4-20250514",
  transcript_ids: [transcript_id],
  context: "A GitLab meeting to discuss logistics",
  answer_format: "TLDR"

}.to_json

lemur_response = http.request(lemur_request)

lemur_result = JSON.parse(lemur_response.body)
puts lemur_result["response"]
````

</Tab>
<Tab language="php" title="PHP">

```php {42-53}
<?php
$base_url = "https://api.assemblyai.com";
$headers = array(
    "authorization: <YOUR_API_KEY>",
    "content-type: application/json"
);

$upload_url = "https://assembly.ai/meeting.mp4";

$ch = curl_init($base_url . "/v2/transcript");
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode(["audio_url" => $upload_url]),
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

$ch = curl_init($base_url . "/lemur/v3/generate/summary");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_POSTFIELDS => json_encode([
        'final_model' => 'anthropic/claude-sonnet-4-20250514',
        'transcript_ids' => [$transcript_id],
        'context' => 'A GitLab meeting to discuss logistics',
        'answer_format' => 'TLDR'
    ])
]);

$response = curl_exec($ch);
$result = json_decode($response, true);
echo $result['response'];
curl_close($ch);
