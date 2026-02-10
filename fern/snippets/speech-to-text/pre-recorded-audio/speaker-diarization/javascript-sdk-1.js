import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// You can use a local filepath:
// const audioFile = "./example.mp3"

// Or use a publicly-accessible URL:
const audioFile = "https://assembly.ai/wildfires.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  for (const utterance of transcript.utterances!) {
    console.log(`Speaker ${utterance.speaker}: ${utterance.text}`);
  }
};

run();
