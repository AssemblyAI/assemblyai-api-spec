import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/phone-msg.m4a";

async function transcribeAndFormat() {
  // Submit transcription request (without formatting)
  const transcript = await client.transcripts.transcribe({
    audio: audioUrl,
    speaker_labels: true,
  });

  console.log(`Transcription completed! ID: ${transcript.id}`);

  // Add custom formatting configuration to the completed transcript
  const understandingConfig = {
    custom_formatting: {
      date: "mm/dd/yyyy",
      phone_number: "(xxx)xxx-xxxx",
      email: "username@domain.com",
      format_utterances: true,
    },
  };

  // Send to Speech Understanding API for formatting
  const result = await client.transcripts.understanding(
    transcript.id,
    understandingConfig
  );

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
