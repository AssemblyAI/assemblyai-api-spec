import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// You can use a local filepath:
const audioFile = "./bilingual-audio.mp3";

// Or use a publicly-accessible URL:
// const audioFile = "<AUDIO_URL>";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  language_detection_options: {
    code_switching: true,
    code_switching_confidence_threshold: 0.5, // Optional parameter - this is set to 0.3 by default
  },
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  if (transcript.status === "error") {
    console.error(`Transcription failed: ${transcript.error}`);
    process.exit(1);
  }

  console.log(`\nFull Transcript:\n\n${transcript.text}\n`);
};

run();
