import { AssemblyAI } from "assemblyai";

// Set your API key
const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// Or use a publicly-accessible URL
const audioUrl = "https://assembly.ai/wildfires.mp3";

async function translateTranscript() {
  // Configure and transcribe the audio

  const transcript = await client.transcripts.transcribe({
    audio: audioUrl,
    speaker_labels: true, // Optional: enable speaker diarization
    // language_detection: true,  // Enable language detection if you are processing files in a variety of languages
  });

  if (transcript.status === "error") {
    throw new Error(`Transcription failed: ${transcript.error}`);
  }

  console.log("Transcription completed!");

  // Request translation using Speech Understanding

  const result = await transcript.speechUnderstanding({
    translation: {
      target_languages: ["es", "de"], // Translate to Spanish and German
      formal: true, // Use formal language style
      match_original_utterance: true, // Get translated utterances (if speaker_labels was enabled)
    },
  });

  // Access and display results
  console.log("\n--- Original Transcript ---");
  console.log(result.text.substring(0, 200) + "..");

  console.log("--- Translations ---");
  for (const [languageCode, translatedText] of Object.entries(
    result.translated_texts
  )) {
    console.log(`${languageCode.toUpperCase()}:`);
    console.log(translatedText.substring(0, 200) + "..");
  }
}

translateTranscript().catch(console.error);
