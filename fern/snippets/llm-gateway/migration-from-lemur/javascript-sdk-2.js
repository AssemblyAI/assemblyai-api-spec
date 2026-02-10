import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

const run = async () => {
  // Step 1: Transcribe an audio file
  const audioFile = "https://assembly.ai/call.mp4";
  const transcript = await client.transcripts.transcribe({ audio: audioFile });

  // Step 2: Prepare for LLM Gateway
  const prompt = "What was the emotional sentiment of the phone call?";

  const response = await fetch(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    {
      method: "POST",
      headers: {
        authorization: "<YOUR_API_KEY>",
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        messages: [
          {
            role: "user",
            content: `Analyze this phone call transcript for emotional sentiment:\n\n${transcript.text}\n\n${prompt}`,
          },
        ],
        max_tokens: 1000,
      }),
    }
  );

  const result = await response.json();
  console.log(result.choices[0].message.content);
};

run();
