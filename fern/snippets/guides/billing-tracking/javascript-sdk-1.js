import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// Add customer_id as a query parameter to your webhook URL
const webhookUrl = "https://your-domain.com/webhook?customer_id=customer_123";

const transcript = await client.transcripts.submit({
  audio: "https://example.com/audio.mp3",
  speech_model: "best",
  webhook_url: webhookUrl,
});
