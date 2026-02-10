import { AssemblyAI } from "assemblyai";
import fs from "fs";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// const audioFile = './local_file.mp3'
const audioFile = "https://assembly.ai/wildfires.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  let srt = await client.transcripts.subtitles(transcript.id, "srt", 32);
  fs.writeFileSync(`transcript_${transcript.id}.srt`, srt);

  // let vtt = await client.transcripts.subtitles(transcript.id, 'vtt', 32)
  // fs.writeFileSync(`transcript_${transcript.id}.vtt`, vtt)
};

run();
