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
  entity_detection: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  for (const entity of transcript.entities) {
    console.log(entity.text);
    console.log(entity.entity_type);
    console.log(`Timestamp: ${entity.start} - ${entity.end}\n`);
  }
};

run();
