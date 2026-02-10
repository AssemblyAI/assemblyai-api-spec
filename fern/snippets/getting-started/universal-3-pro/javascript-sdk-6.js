import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assemblyaiassets.com/audios/entity_accuracy.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  prompt:
    "The speaker is discussing the cancer drug Anktiva (spelled A-N-K-T-I-V-A). When you hear what sounds like Entiva or similar pronunciations, transcribe it as Anktiva. This is the correct pharmaceutical name.",
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log(transcript.text);
};

run();
