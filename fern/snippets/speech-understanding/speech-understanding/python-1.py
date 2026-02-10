import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
"authorization": "<YOUR_API_KEY>"
}

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file

upload_url = "https://assembly.ai/wildfires.mp3"

# Configure transcript with speaker identification

data = {
"audio_url": upload_url,
"speech_models": ["universal-3-pro", "universal-2"],
"language_detection": True,
"speaker_labels": True,
"speech_understanding": {
"request": {
"speaker_identification": {
"speaker_type": "name",
"known_values": ["Michel Martin", "Peter DeCarlo"] # Change these values to match the names of the speakers in your file
}
}
}
}

# Submit the transcription request

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

# Poll for transcription results

while True:
transcript = requests.get(polling_endpoint, headers=headers).json()

if transcript["status"] == "completed":
break

elif transcript["status"] == "error":
raise RuntimeError(f"Transcription failed: {transcript['error']}")

else:
time.sleep(3)

# Access the results and print utterances to the terminal

for utterance in transcript["utterances"]:
print(f"{utterance['speaker']}: {utterance['text']}")

````

</Tab>

{/* <Tab language="python-sdk" title="Python SDK">
```python
import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/wildfires.mp3"

# Configure transcript with speaker identification
config = aai.TranscriptionConfig(
  speaker_labels=True,
  speech_understanding=aai.SpeechUnderstandingConfig(
    speaker_identification=aai.SpeakerIdentificationConfig(
      speaker_type="name",
      known_values=["Michel Martin", "Peter DeCarlo"]  # Change these values to match the names of the speakers in your file
    )
  )
)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_url, config)

# Access the results and print utterances to the terminal
for utterance in transcript.utterances:
  print(f"{utterance.speaker}: {utterance.text}")
````

</Tab> */}

<Tab language="javascript" title="JavaScript">
```javascript
const baseUrl = "https://api.assemblyai.com";

const headers = {
"authorization": "<YOUR_API_KEY>",
"content-type": "application/json"
};

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const uploadUrl = "https://assembly.ai/wildfires.mp3";

// Configure transcript with speaker identification
const data = {
audio_url: uploadUrl,
speech_models: ["universal-3-pro", "universal-2"],
language_detection: true,
speaker_labels: true,
speech_understanding: {
request: {
speaker_identification: {
speaker_type: "name",
known_values: ["Michel Martin", "Peter DeCarlo"] // Change these values to match the names of the speakers in your file
}
}
}
};

async function main() {
// Submit the transcription request
const response = await fetch(`${baseUrl}/v2/transcript`, {
method: "POST",
headers: headers,
body: JSON.stringify(data)
});

const { id: transcriptId } = await response.json();
const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

// Poll for transcription results
while (true) {
const pollingResponse = await fetch(pollingEndpoint, { headers });
const transcript = await pollingResponse.json();

    if (transcript.status === "completed") {
      // Access the results and print utterances to the console
      for (const utterance of transcript.utterances) {
        console.log(`${utterance.speaker}: ${utterance.text}`);
      }
      break;
    } else if (transcript.status === "error") {
      throw new Error(`Transcription failed: ${transcript.error}`);
    } else {
      await new Promise(resolve => setTimeout(resolve, 3000));
    }

}
}

main().catch(console.error);

````

</Tab>

{/* <Tab language="javascript-sdk" title="JavaScript SDK">
```javascript
import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>"
});

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/wildfires.mp3";

// Configure transcript with speaker identification
const config = {
  audio_url: audioUrl,
  speaker_labels: true,
  speech_understanding: {
    speaker_identification: {
      speaker_type: "name",
      known_values: ["Michel Martin", "Peter DeCarlo"]  // Change these values to match the names of the speakers in your file
    }
  }
};

const transcript = await client.transcripts.transcribe(config);

// Access the results and print utterances to the console
for (const utterance of transcript.utterances) {
  console.log(`${utterance.speaker}: ${utterance.text}`);
}
````

</Tab> */}
</Tabs>

### Method 2: Transcribe and identify in separate requests

This method is useful when you already have a completed transcript or for more complex workflows where you need to separate transcription from speaker identification.

<Tabs groupId="language">
<Tab language="python" title="Python" default>
```python
import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
"authorization": "<YOUR_API_KEY>"
}

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file

upload_url = "https://assembly.ai/wildfires.mp3"

data = {
"audio_url": upload_url,
"speech_models": ["universal-3-pro", "universal-2"],
"language_detection": True,
"speaker_labels": True
}

# Transcribe file

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

# Poll for transcription results

while True:
transcript = requests.get(polling_endpoint, headers=headers).json()

if transcript["status"] == "completed":
break

elif transcript["status"] == "error":
raise RuntimeError(f"Transcription failed: {transcript['error']}")

else:
time.sleep(3)

# Enable speaker identification

understanding_body = {
"transcript_id": transcript_id,
"speech_understanding": {
"request": {
"speaker_identification": {
"speaker_type": "name",
"known_values": ["Michel Martin", "Peter DeCarlo"] # Change these values to match the names of the speakers in your file
}
}
}
}

# Send the modified transcript to the Speech Understanding API

result = requests.post(
"https://llm-gateway.assemblyai.com/v1/understanding",
headers = headers,
json = understanding_body
).json()

# Access the results and print utterances to the terminal

for utterance in result["utterances"]:
print(f"{utterance['speaker']}: {utterance['text']}")

````

</Tab>

{/* <Tab language="python-sdk" title="Python SDK">
```python
import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(speaker_labels=True)
transcript = aai.Transcriber().transcribe(audio_url, config)

# Enable speaker identification
understanding_config = aai.SpeechUnderstandingConfig(
  speaker_identification=aai.SpeakerIdentificationConfig(
    speaker_type="name",
    known_values=["Michel Martin", "Peter DeCarlo"]  # Change these values to match the names of the speakers in your file
  )
)

result = aai.SpeechUnderstanding().understand(
  transcript.id,
  understanding_config
)

# Access the results and print utterances to the terminal
for utterance in result.utterances:
  print(f"{utterance.speaker}: {utterance.text}")
````

</Tab> */}

<Tab language="javascript" title="JavaScript">
```javascript
const baseUrl = "https://api.assemblyai.com";
const apiKey = "<YOUR_API_KEY>";

const headers = {
"authorization": apiKey,
"content-type": "application/json"
};

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const uploadUrl = "https://assembly.ai/wildfires.mp3";

async function transcribeAndIdentifySpeakers() {
// Transcribe file
const transcriptResponse = await fetch(`${baseUrl}/v2/transcript`, {
method: 'POST',
headers: headers,
body: JSON.stringify({
audio_url: uploadUrl,
speaker_labels: true
})
});

const { id: transcriptId } = await transcriptResponse.json();
const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

// Poll for transcription results
while (true) {
const pollingResponse = await fetch(pollingEndpoint, { headers });
const transcript = await pollingResponse.json();

    if (transcript.status === "completed") {
      break;
    } else if (transcript.status === "error") {
      throw new Error(`Transcription failed: ${transcript.error}`);
    } else {
      await new Promise(resolve => setTimeout(resolve, 3000));
    }

}

// Enable speaker identification
const understandingBody = {
transcript_id: transcriptId,
speech_understanding: {
request: {
speaker_identification: {
speaker_type: "name",
known_values: ["Michel Martin", "Peter DeCarlo"] // Change these values to match the names of the speakers in your file
}
}
}
};

// Send the modified transcript to the Speech Understanding API
const understandingResponse = await fetch(
"https://llm-gateway.assemblyai.com/v1/understanding",
{
method: 'POST',
headers: headers,
body: JSON.stringify(understandingBody)
}
);

const result = await understandingResponse.json();

// Access the results and print utterances to the terminal
for (const utterance of result.utterances) {
console.log(`${utterance.speaker}: ${utterance.text}`);
}
}

transcribeAndIdentifySpeakers();

````

</Tab>

{/* <Tab language="javascript-sdk" title="JavaScript SDK">
```javascript
const { AssemblyAI } = require('assemblyai');

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>"
});

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/wildfires.mp3";

async function transcribeAndIdentifySpeakers() {
  const transcript = await client.transcripts.transcribe({
    audio_url: audioUrl,
    speaker_labels: true
  });

  // Enable speaker identification
  const result = await client.speechUnderstanding.understand({
    transcript_id: transcript.id,
    speech_understanding: {
      request: {
        speaker_identification: {
          speaker_type: "name",
          known_values: ["Michel Martin", "Peter DeCarlo"]  // Change these values to match the names of the speakers in your file
        }
      }
    }
  });

  // Access the results and print utterances to the terminal
  for (const utterance of result.utterances) {
    console.log(`${utterance.speaker}: ${utterance.text}`);
  }
}

transcribeAndIdentifySpeakers();
````

</Tab> */}
</Tabs>

### Output format details

Here is how the structure of the utterances in the `utterances` key differs when Speaker Diarization is used versus when Speaker Identification is used:

**Before (Speaker Diarization only):**

```txt wordWrap
Speaker A: ... We wanted to better understand what's happening here and why, so we called Peter DeCarlo, an associate professor in the Department of Environmental Health and Engineering at Johns Hopkins University. Good morning, Professor.
Speaker B: Good morning.
Speaker A: So what is it about the conditions right now that have caused this round of wildfires to affect so many people so far away?
Speaker B: Well, there's a couple of things. The season has been pretty dry already, and then the fact that we're getting hit in the US is because there's a couple weather systems that are essentially channeling the smoke from those Canadian wildfires through Pennsylvania into the mid Atlantic and the Northeast and kind of just dropping the smoke there.
