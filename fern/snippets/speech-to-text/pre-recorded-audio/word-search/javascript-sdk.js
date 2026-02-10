import { AssemblyAI } from "assemblyai";

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

  // Set the words you want to search for.
  const words = ["foo", "bar", "foo bar", "42"];

  const { matches } = await client.transcripts.wordSearch(transcript.id, words);

  for (const match of matches) {
    console.log(`Found '${match.text}' ${match.count} times in the transcript`);
  }
};

run();
