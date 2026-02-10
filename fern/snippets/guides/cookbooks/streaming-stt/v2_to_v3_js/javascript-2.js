const API_KEY = "<YOUR_API_KEY>";
const SAMPLE_RATE = 16000; // 16kHz sample rate

const ws = new WebSocket(
  `wss://api.assemblyai.com/v2/realtime/ws?sample_rate=${SAMPLE_RATE}`,
  {
    headers: {
      Authorization: API_KEY,
    },
  }
);
