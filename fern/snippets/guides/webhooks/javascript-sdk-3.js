import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// const audioFile = './local_file.mp3'
const audioFile = "https://assembly.ai/wildfires.mp3";

const params = {
  audio: audioFile,
  webhook_url: "https://example.com/webhook",
  webhook_auth_header_name: "X-My-Webhook-Secret",
  webhook_auth_header_value: "secret-value",
};

const run = async () => {
  const transcript = await client.transcripts.submit(params);
};

run();
