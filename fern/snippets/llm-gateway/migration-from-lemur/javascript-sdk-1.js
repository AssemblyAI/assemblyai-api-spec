import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const run = async () => {
  // Step 1: Transcribe an audio file
  const audioFile = "https://assembly.ai/call.mp4";
  const transcript = await client.transcripts.transcribe({ audio: audioFile });

  // Step 2: Apply LeMUR
  const prompt = "What was the emotional sentiment of the phone call?";
  const { response } = await client.lemur.task({
    transcript_ids: [transcript.id],
    prompt,
    final_model: "anthropic/claude-sonnet-4-20250514",
  });

  console.log(response);
};

run();
