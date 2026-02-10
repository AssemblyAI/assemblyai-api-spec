import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "YOUR_API_KEY",
});

const transcriber = client.streaming.transcriber({
  sampleRate: 16_000,
  apiHost: "streaming.eu.assemblyai.com", // EU streaming endpoint
});
