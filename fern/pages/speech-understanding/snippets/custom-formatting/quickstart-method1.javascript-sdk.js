import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/phone-msg.m4a";

// Configure transcription with custom formatting
const config = {
  audio_url: audioUrl,
  speaker_labels: true,
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

// Submit transcription and wait for results
const transcript = await client.transcripts.transcribe(config);

// Access and display results
console.log("\n--- Formatting Details ---");
const mapping =
  transcript.speech_understanding.response.custom_formatting.mapping;
for (const [original, formatted] of Object.entries(mapping)) {
  console.log(`Original: ${original}`);
  console.log(`Formatted: ${formatted}\n`);
}
