import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assemblyaiassets.com/audios/ouput_formatting.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  prompt:
    "Add punctuation based on the speaker's tone and expressiveness. Use exclamation marks (!) when the speaker is yelling, excited, or emphatic. Use question marks (?) for questioning intonation. Apply standard punctuation (periods, commas) based on natural speech patterns and pauses.",
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log(transcript.text);
};

run();
