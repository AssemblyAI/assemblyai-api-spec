import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile =
  "https://assemblyaiassets.com/audios/code_switching_multilingual.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  prompt:
    "The spoken language may change throughout the audio, transcribe in the original language mix (code-switching), preserving the words in the language they are spoken.",
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log(transcript.text);
};

run();
