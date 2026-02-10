import fetch from "node-fetch";

const baseUrl = "https://api.assemblyai.com";
const headers = {
  authorization: "YOUR_API_KEY",
};

const audioUrl = "https://assembly.ai/wildfires.mp3";

// Configure transcription with translation and speaker labels
const data = {
  audio_url: audioUrl,
  speaker_labels: true, // Enable speaker labels
  // language_detection: true,  // Enable language detection if you are processing files in a variety of languages
  speech_understanding: {
    request: {
      translation: {
        target_languages: ["es"],
        match_original_utterance: true, // Get translated text per utterance
        formal: true,
      },
    },
  },
};

async function transcribeWithTranslatedUtterances() {
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
      // Access translated utterances
      for (const utterance of transcriptResult.utterances) {
        console.log(`Speaker ${utterance.speaker}:`);
        console.log(`  Original: ${utterance.text.substring(0, 100)}...`);
        console.log(
          `  Spanish: ${utterance.translated_texts.es.substring(0, 100)}...`
        );
        console.log();
      }
      break;
    } else if (transcriptResult.status === "error") {
      throw new Error(`Transcription failed: ${transcriptResult.error}`);
    } else {
      await new Promise((resolve) => setTimeout(resolve, 3000));
    }
  }
}

transcribeWithTranslatedUtterances();
