import fetch from "node-fetch";

const baseUrl = "https://api.assemblyai.com";
const headers = {
  authorization: "YOUR_API_KEY",
};

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/wildfires.mp3";

// Configure transcription with translation
const data = {
  audio_url: audioUrl,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true, // Enable speaker labels
  speech_understanding: {
    request: {
      translation: {
        target_languages: ["es", "de"], // Translate to Spanish and German
        formal: true, // Use formal language style
      },
    },
  },
};

// Submit transcription request
async function transcribeAndTranslate() {
  const response = await fetch(`${baseUrl}/v2/transcript`, {
    method: "POST",
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const transcript = await response.json();
  const transcriptId = transcript.id;
  const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

  // Poll transcription results
  while (true) {
    const pollingResponse = await fetch(pollingEndpoint, { headers });
    const transcriptResult = await pollingResponse.json();

    if (transcriptResult.status === "completed") {
      // Access and display results
      console.log("\n--- Original Transcript ---");
      console.log(transcriptResult.text.substring(0, 200) + "...\n");

      console.log("--- Translations ---");
      for (const [languageCode, translatedText] of Object.entries(
        transcriptResult.translated_texts
      )) {
        console.log(`${languageCode.toUpperCase()}:`);
        console.log(translatedText.substring(0, 200) + "...\n");
      }
      break;
    } else if (transcriptResult.status === "error") {
      throw new Error(`Transcription failed: ${transcriptResult.error}`);
    } else {
      await new Promise((resolve) => setTimeout(resolve, 3000));
    }
  }
}

transcribeAndTranslate();
