import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const transcript = await client.transcripts.get("<TRANSCRIPT_ID>");

if (transcript.status === "error") {
  throw new Error(`Transcription failed: ${transcript.error}`);
}

console.log(transcript.text);
