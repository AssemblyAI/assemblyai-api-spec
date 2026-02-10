import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// Get transcript using the ID from webhook
const transcript = await client.transcripts.get("<TRANSCRIPT_ID>");

if (transcript.status === "completed") {
  const audioDuration = transcript.audio_duration; // Duration in seconds
  // Use audioDuration for billing/tracking
}
