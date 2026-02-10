import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const run = async () => {
  // Step 1: Transcribe an audio file.
  // const audioFile = './local_file.mp4'
  // Or use a publicly-accessible URL:
  const audioFile = "https://assembly.ai/call.mp4";
  const transcript = await client.transcripts.transcribe({ audio: audioFile });

  // Step 2: Define your prompt.
  const prompt = "What was the emotional sentiment of the phone call?";

  // Step 3: Apply LeMUR.
  const { response } = await client.lemur.task({
    transcript_ids: [transcript.id],
    prompt,
    final_model: "anthropic/claude-sonnet-4-20250514",
  });

  console.log(response);
};

run();
