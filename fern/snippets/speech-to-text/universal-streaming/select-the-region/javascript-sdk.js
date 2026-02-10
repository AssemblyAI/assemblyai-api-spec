import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
  streamingBaseUrl: "wss://streaming.eu.assemblyai.com",
});

const transcriber = client.streaming.transcriber({
  sampleRate: 16_000,
});

await transcriber.connect();
