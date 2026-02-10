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
  auto_highlights: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  for (const result of transcript.auto_highlights_result.results) {
    const timestamps = result.timestamps
      .map(({ start, end }) => `[Timestamp(start=${start}, end=${end})]`)
      .join(", ");
    console.log(
      `Highlight: ${result.text}, Count: ${result.count}, Rank ${result.rank}, Timestamps: ${timestamps}`
    );
  }
};

run();
