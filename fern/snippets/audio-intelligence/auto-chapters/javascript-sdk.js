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
  auto_chapters: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log("Transcript ID: ", transcript.id);

  for (const chapter of transcript.chapters) {
    console.log(`${chapter.start}-${chapter.end}: ${chapter.headline}`);
  }
};

run();
