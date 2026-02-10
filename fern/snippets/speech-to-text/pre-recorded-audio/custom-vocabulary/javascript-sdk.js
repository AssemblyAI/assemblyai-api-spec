import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// const audioFile = './local_file.mp3'
const audioFile = "https://assembly.ai/wildfires.mp3";

const params = {
  audio: audioFile,
  word_boost: ["aws", "azure", "google cloud"],
  boost_param: "high",
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  console.log(transcript.text);
};

run();
