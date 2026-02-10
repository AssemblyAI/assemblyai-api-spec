import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assemblyaiassets.com/audios/Difficult_audio.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  prompt:
    "When multiple speakers talk simultaneously, mark crosstalk segments.",
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log(transcript.text);
};

run();
