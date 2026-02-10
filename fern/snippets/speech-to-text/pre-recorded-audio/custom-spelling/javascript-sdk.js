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
  custom_spelling: [
    {
      from: ["Decarlo"],
      to: "DeCarlo",
    },
    {
      from: ["Sequel"],
      to: "SQL",
    },
  ],
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  console.log(transcript.text);
};

run();
