import axios from "axios";

const baseUrl = "https://api.assemblyai.com";
const headers = { authorization: "<YOUR_API_KEY>" };

// Add customer_id as a query parameter to your webhook URL
const webhookUrl = "https://your-domain.com/webhook?customer_id=customer_123";

const data = {
  audio_url: "https://example.com/audio.mp3",
  webhook_url: webhookUrl,
};

// Submit without waiting for completion
const response = await axios.post(`${baseUrl}/v2/transcript`, data, {
  headers,
});
const transcriptId = response.data.id;
