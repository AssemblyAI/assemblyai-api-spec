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

  console.log(transcript.text);

  // Print word-level details
  for (const word of transcript.words) {
    console.log(
      `Word: ${word.text}, Start: ${word.start}, End: ${word.end}, Confidence: ${word.confidence}`
    );
  }
};

run();
