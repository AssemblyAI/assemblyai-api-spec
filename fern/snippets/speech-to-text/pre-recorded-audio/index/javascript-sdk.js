import { AssemblyAI } from "assemblyai";

const baseUrl = "https://api.assemblyai.com";

const client = new AssemblyAI({
  apiKey: "YOUR_API_KEY",
  baseUrl: baseUrl,
});

// Use a publicly-accessible URL
const audioFile = "https://assembly.ai/wildfires.mp3";

// Or use a local file:
// const audioFile = "./example.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  if (transcript.status === "error") {
    throw new Error(`Transcription failed: ${transcript.error}`);
  }

  console.log(`\nFull Transcript:\n\n${transcript.text}`);

  // Optionally print speaker diarization results
  // for (const utterance of transcript.utterances) {
  //   console.log(`Speaker ${utterance.speaker}: ${utterance.text}`);
  // }
};

run();
