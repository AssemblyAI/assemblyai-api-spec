const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
  "content-type": "application/json",
};

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/wildfires.mp3";

// Helper function to sleep
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
  // Submit transcription request (without translation)
  const data = {
    audio_url: audioUrl,
    speaker_labels: true,
    // language_detection: true,  // Enable language detection if you are processing files in a variety of languages
  };

  // Transcribe file
  const response = await fetch(`${baseUrl}/v2/transcript`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data),
  });

  const responseData = await response.json();
  const transcriptId = responseData.id;
  const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

  // Poll for transcription completion
  let transcript;
  while (true) {
    const pollResponse = await fetch(pollingEndpoint, {
      method: "GET",
      headers: headers,
    });

    transcript = await pollResponse.json();

    if (transcript.status === "completed") {
      console.log("Transcription completed!");
      break;
    } else if (transcript.status === "error") {
      throw new Error(`Transcription failed: ${transcript.error}`);
    } else {
      await sleep(3000);
    }
  }

  // Add translation configuration to the completed transcript
  const understandingBody = {
    transcript_id: transcriptId,
    speech_understanding: {
      request: {
        translation: {
          target_languages: ["es", "de"], // Translate to Spanish and German
          formal: true, // Use formal language style
        },
      },
    },
  };

  // Send to Speech Understanding API for translation
  const resultResponse = await fetch(
    "https://llm-gateway.assemblyai.com/v1/understanding",
    {
      method: "POST",
      headers: headers,
      body: JSON.stringify(understandingBody),
    }
  );

  const result = await resultResponse.json();

  // Access and display results
  console.log("\n--- Original Transcript ---");
  console.log(transcript.text.substring(0, 200) + "...\n");

  console.log("--- Translations ---");
  for (const [languageCode, translatedText] of Object.entries(
    result.translated_texts
  )) {
    console.log(`${languageCode.toUpperCase()}:`);
    console.log(translatedText.substring(0, 200) + "...\n");
  }
}

// Run the main function
main().catch((error) => {
  console.error("Error:", error);
});
