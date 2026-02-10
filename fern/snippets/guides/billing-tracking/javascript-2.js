import axios from "axios";

const baseUrl = "https://api.assemblyai.com";
const headers = { authorization: "<YOUR_API_KEY>" };

// Get transcript using the ID from webhook
const response = await axios.get(`${baseUrl}/v2/transcript/<TRANSCRIPT_ID>`, {
  headers,
});
const transcript = response.data;

if (transcript.status === "completed") {
  const audioDuration = transcript.audio_duration; // Duration in seconds
  // Use audioDuration for billing/tracking
}
