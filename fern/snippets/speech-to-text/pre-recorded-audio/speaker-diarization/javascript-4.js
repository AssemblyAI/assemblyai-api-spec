const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
  "content-type": "application/json",
};

const audioUrl = "https://assembly.ai/wildfires.mp3";

// Configure transcript with speaker diarization and speaker identification
const data = {
  audio_url: audioUrl,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true,
  speech_understanding: {
    request: {
      speaker_identification: {
        speaker_type: "name",
        known_values: ["Michel Martin", "Peter DeCarlo"],
      },
    },
  },
};

async function main() {
  // Submit the transcription request
  const response = await fetch(`${baseUrl}/v2/transcript`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data),
  });

  const { id: transcriptId } = await response.json();
  const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

  // Poll for transcription results
  while (true) {
    const pollingResponse = await fetch(pollingEndpoint, { headers });
    const transcript = await pollingResponse.json();

    if (transcript.status === "completed") {
      // Print utterances with identified speaker names
      for (const utterance of transcript.utterances) {
        console.log(`${utterance.speaker}: ${utterance.text}`);
      }
      break;
    } else if (transcript.status === "error") {
      throw new Error(`Transcription failed: ${transcript.error}`);
    } else {
      await new Promise((resolve) => setTimeout(resolve, 3000));
    }
  }
}

main().catch(console.error);
