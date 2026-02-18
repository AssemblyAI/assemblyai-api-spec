import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "YOUR_API_KEY",
});

// Configure transcription with translation
const config = {
  audio_url: "https://assembly.ai/wildfires.mp3",
  speaker_labels: true, // Enable speaker labels
  //  language_detection: true,  // Enable language detection if you are processing files in a variety of languages
  speech_understanding: {
    request: {
      translation: {
        target_languages: ["es", "de"], // Translate to Spanish and German
        formal: true, // Use formal language style
        match_original_utterance: true, // Get translated utterances
      },
    },
  },
};

// Submit transcription request
const transcript = await client.transcripts.transcribe(config);

// Access and display results
console.log("\n--- Original Transcript ---");
console.log(transcript.text?.substring(0, 200) + "...\n");

console.log("\n--- Translations ---");
if (transcript.translated_texts) {
  for (const [languageCode, translatedText] of Object.entries(
    transcript.translated_texts
  )) {
    console.log(`${languageCode.toUpperCase()}:`);
    console.log(translatedText.substring(0, 200) + "...\n");
  }
}
