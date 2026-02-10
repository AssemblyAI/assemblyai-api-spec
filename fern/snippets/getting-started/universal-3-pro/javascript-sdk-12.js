import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assemblyaiassets.com/audios/nlp_prompting.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  prompt:
    "Produce a transcript for a clinical history evaluation. It's important to capture medication and dosage accurately. Every disfluency is meaningful data. Include: fillers (um, uh, er, erm, ah, hmm, mhm, like, you know, I mean), repetitions (I I I, the the), restarts (I was- I went), stutters (th-that, b-but, no-not), and informal speech (gonna, wanna, gotta)",
  temperature: 0.1,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log(transcript.text);
};

run();
