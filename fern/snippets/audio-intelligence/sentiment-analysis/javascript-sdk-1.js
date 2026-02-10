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
  sentiment_analysis: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log("Transcript ID: ", transcript.id);

  for (const result of transcript.sentiment_analysis_results) {
    console.log(result.text);
    console.log(result.sentiment); // POSITIVE, NEUTRAL, or NEGATIVE
    console.log(result.confidence);
    console.log(`Timestamp: ${result.start} - ${result.end}`);
  }
};
run();
