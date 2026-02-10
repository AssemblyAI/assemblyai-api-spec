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
  iab_categories: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log("Transcript ID: ", transcript.id);

  // Get the parts of the transcript that were tagged with topics
  for (const result of transcript.iab_categories_result.results) {
    console.log(result.text);
    console.log(
      `Timestamp: ${result.timestamp?.start} - ${result.timestamp?.end}`
    );
    for (const label of result.labels) {
      console.log(`${label.label} (${label.relevance})`);
    }
  }

  // Get a summary of all topics in the transcript
  for (const [topic, relevance] of Object.entries(
    transcript.iab_categories_result.summary
  )) {
    console.log(`Audio is ${relevance * 100} relevant to ${topic}`);
  }
};

run();
