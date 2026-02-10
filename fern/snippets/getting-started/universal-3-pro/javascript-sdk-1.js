import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assembly.ai/sports_injuries.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log(transcript.text);
};

run();
