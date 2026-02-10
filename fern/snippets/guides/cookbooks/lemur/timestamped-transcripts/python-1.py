import requests
import json
import time

API_KEY = "YOUR_API_KEY"
headers = {"authorization": API_KEY}

# Transcribe the audio file

print("Submitting audio for transcription...")
transcript_response = requests.post(
"https://api.assemblyai.com/v2/transcript",
headers=headers,
json={
"audio_url": "https://assembly.ai/wildfires.mp3",
"speaker_labels": True
}
)

transcript_id = transcript_response.json()["id"]

# Poll for transcription completion

while True:
transcript_result = requests.get(
f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
headers=headers
).json()

    if transcript_result["status"] == "completed":
        break
    elif transcript_result["status"] == "error":
        raise Exception(f"Transcription failed: {transcript_result['error']}")

    time.sleep(3)

# Extract utterances with timestamps

utterances_data = [
{"text": u["text"], "start": u["start"], "end": u["end"], "speaker": u["speaker"]}
for u in transcript_result["utterances"]
]

# Create prompt with timestamped utterances

prompt = f"""You are analyzing a transcript with timestamped utterances. Each utterance includes the text content, speaker label, and start/end timestamps in milliseconds.

Here is the transcript data:
{json.dumps(utterances_data, indent=2)}

Task: Identify the 3-5 most engaging, impactful, or quotable utterances from this transcript.

Return your response as a JSON array with the following structure:
{{
  "quotes": [
    {{
      "text": "exact quote text",
      "start": start_timestamp_in_milliseconds,
      "end": end_timestamp_in_milliseconds,
      "speaker": "speaker_label",
      "reason": "brief explanation of why this quote is engaging"
    }}
]
}}

Return ONLY valid JSON, no additional text."""

# Use LLM Gateway to extract quotes

print("Submitting transcript to LLM Gateway for quote extraction...")
gateway_response = requests.post(
"https://llm-gateway.assemblyai.com/v1/chat/completions",
headers=headers,
json={
"model": "gpt-5-nano",
"messages": [
{"role": "user", "content": prompt}
]
}
)

result = gateway_response.json()
quotes_json = json.loads(result["choices"][0]["message"]["content"])
print(json.dumps(quotes_json, indent=2))

````

</Tab>
<Tab title="JavaScript">
```javascript
const API_KEY = "YOUR_API_KEY";

const headers = {
  "authorization": API_KEY,
  "content-type": "application/json"
};

// Transcribe the audio file
console.log("Submitting audio for transcription...");
const transcriptResponse = await fetch(
  "https://api.assemblyai.com/v2/transcript",
  {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
      audio_url: "https://assembly.ai/wildfires.mp3",
      speaker_labels: true
    })
  }
);

const { id: transcriptId } = await transcriptResponse.json();

// Poll for transcription completion
let transcriptResult;
while (true) {
  const response = await fetch(
    `https://api.assemblyai.com/v2/transcript/${transcriptId}`,
    { headers }
  );
  transcriptResult = await response.json();

  if (transcriptResult.status === "completed") {
    break;
  } else if (transcriptResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptResult.error}`);
  }

  await new Promise(resolve => setTimeout(resolve, 3000));
}

// Extract utterances with timestamps
const utterancesData = transcriptResult.utterances.map(u => ({
  text: u.text,
  start: u.start,
  end: u.end,
  speaker: u.speaker
}));

// Create prompt with timestamped utterances
const prompt = `You are analyzing a transcript with timestamped utterances. Each utterance includes the text content, speaker label, and start/end timestamps in milliseconds.

Here is the transcript data:
${JSON.stringify(utterancesData, null, 2)}

Task: Identify the 3-5 most engaging, impactful, or quotable utterances from this transcript.

Return your response as a JSON array with the following structure:
{
  "quotes": [
    {
      "text": "exact quote text",
      "start": start_timestamp_in_milliseconds,
      "end": end_timestamp_in_milliseconds,
      "speaker": "speaker_label",
      "reason": "brief explanation of why this quote is engaging"
    }
  ]
}

Return ONLY valid JSON, no additional text.`;

// Use LLM Gateway to extract quotes
console.log("Submitting transcript to LLM Gateway for quote extraction...");
const gatewayResponse = await fetch(
  "https://llm-gateway.assemblyai.com/v1/chat/completions",
  {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
      model: "gpt-5-nano",
      messages: [
        { role: "user", content: prompt }
      ]
    })
  }
);

const result = await gatewayResponse.json();
const quotesJson = JSON.parse(result.choices[0].message.content);
console.log(JSON.stringify(quotesJson, null, 2));
````

</Tab>
</Tabs>

## Getting Started

Before we begin, make sure you have an AssemblyAI account and an API key. You can [sign up](https://www.assemblyai.com/dashboard/signup/) for an AssemblyAI account and get your API key from your [dashboard](https://www.assemblyai.com/app/account).

## Step-by-Step Instructions

### Step 1: Set up your API key and headers

<Tabs>
<Tab title="Python">
```python
import requests
import json
import time

API_KEY = "YOUR_API_KEY"
headers = {"authorization": API_KEY}

````

</Tab>
<Tab title="JavaScript">
```javascript
const API_KEY = "YOUR_API_KEY";

const headers = {
  "authorization": API_KEY,
  "content-type": "application/json"
};
````

</Tab>
</Tabs>

### Step 2: Transcribe the audio file

Next, we'll use AssemblyAI to transcribe a file and save our transcript for later use. We'll enable `speaker_labels` to get utterances grouped by speaker.

<Tabs>
<Tab title="Python">
```python
# Transcribe the audio file
print("Submitting audio for transcription...")
transcript_response = requests.post(
    "https://api.assemblyai.com/v2/transcript",
    headers=headers,
    json={
        "audio_url": "https://assembly.ai/wildfires.mp3",
        "speaker_labels": True
    }
)

transcript_id = transcript_response.json()["id"]

# Poll for transcription completion

while True:
transcript_result = requests.get(
f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
headers=headers
).json()

    if transcript_result["status"] == "completed":
        break
    elif transcript_result["status"] == "error":
        raise Exception(f"Transcription failed: {transcript_result['error']}")

    time.sleep(3)

````

</Tab>
<Tab title="JavaScript">
```javascript
// Transcribe the audio file
console.log("Submitting audio for transcription...");
const transcriptResponse = await fetch(
  "https://api.assemblyai.com/v2/transcript",
  {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
      audio_url: "https://assembly.ai/wildfires.mp3",
      speaker_labels: true
    })
  }
);

const { id: transcriptId } = await transcriptResponse.json();

// Poll for transcription completion
let transcriptResult;
while (true) {
  const response = await fetch(
    `https://api.assemblyai.com/v2/transcript/${transcriptId}`,
    { headers }
  );
  transcriptResult = await response.json();

  if (transcriptResult.status === "completed") {
    break;
  } else if (transcriptResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptResult.error}`);
  }

  await new Promise(resolve => setTimeout(resolve, 3000));
}
````

</Tab>
</Tabs>

### Step 3: Extract utterances with timestamps

Then we'll take the timestamped `utterances` array from our transcript and format it as structured data. Utterances are grouped by speaker and include continuous speech segments.

<Tabs>
<Tab title="Python">
```python
utterances_data = [
    {"text": u["text"], "start": u["start"], "end": u["end"], "speaker": u["speaker"]} 
    for u in transcript_result["utterances"]
]
