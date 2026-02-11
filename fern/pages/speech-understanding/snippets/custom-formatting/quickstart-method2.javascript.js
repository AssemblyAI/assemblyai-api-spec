const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
  "content-type": "application/json",
};

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/phone-msg.m4a";

// Submit transcription request (without formatting)
const data = {
  audio_url: audioUrl,
  speaker_labels: true,
};

async function transcribeAndFormat() {
  // Start transcription
  const response = await fetch(`${baseUrl}/v2/transcript`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data),
  });

  const { id: transcriptId } = await response.json();
  const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

  // Poll for transcription completion
  while (true) {
    const pollingResponse = await fetch(pollingEndpoint, { headers });
    const transcript = await pollingResponse.json();

    if (transcript.status === "completed") {
      console.log("Transcription completed!");
      break;
    } else if (transcript.status === "error") {
      throw new Error(`Transcription failed: ${transcript.error}`);
    } else {
      await new Promise((resolve) => setTimeout(resolve, 3000));
    }
  }

  // Add custom formatting configuration to the completed transcript
  const understandingBody = {
    transcript_id: transcriptId,
    speech_understanding: {
      request: {
        custom_formatting: {
          date: "mm/dd/yyyy",
          phone_number: "(xxx)xxx-xxxx",
          email: "username@domain.com",
          format_utterances: true,
        },
      },
    },
  };

  // Send to Speech Understanding API for formatting
  const understandingResponse = await fetch(
    "https://llm-gateway.assemblyai.com/v1/understanding",
    {
      method: "POST",
      headers: headers,
      body: JSON.stringify(understandingBody),
    }
  );

  const result = await understandingResponse.json();

  // Access and display results
  console.log("\n--- Formatting Details ---");
  const mapping =
    result.speech_understanding.response.custom_formatting.mapping;
  for (const [original, formatted] of Object.entries(mapping)) {
    console.log(`Original: ${original}`);
    console.log(`Formatted: ${formatted}\n`);
  }
}

transcribeAndFormat();
