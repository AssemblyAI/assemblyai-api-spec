// --- Configuration ---
const YOUR_API_KEY = "YOUR-API-KEY"; // Replace with your actual API key
const CONNECTION_PARAMS = {
  sample_rate: 16000,
  format_turns: true, // Request formatted final transcripts
};
const API_ENDPOINT_BASE_URL = "wss://streaming.assemblyai.com/v3/ws";
const API_ENDPOINT = `${API_ENDPOINT_BASE_URL}?${querystring.stringify(CONNECTION_PARAMS)}`;

// Initialize WebSocket connection
ws = new WebSocket(API_ENDPOINT, {
  headers: {
    Authorization: YOUR_API_KEY,
  },
});
