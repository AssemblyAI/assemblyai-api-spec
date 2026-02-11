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