import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const audioFile = "https://assemblyaiassets.com/audios/speaker_diarization.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true,
  prompt: "Produce a transcript with every disfluency data. Additionally, label speakers with their respective roles. 1. Place [Speaker:role] at the start of each speaker turn. Example format: [Speaker:NURSE] Hello there. How can I help you today? [Speaker:PATIENT] I'm feeling unwell. I have a headache.",
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  for (const utterance of transcript.utterances!) {
    console.log(`Speaker ${utterance.speaker}: ${utterance.text}`);
  }
};

run();
