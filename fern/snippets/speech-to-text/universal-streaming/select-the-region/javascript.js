const WebSocket = require("ws");
const querystring = require("querystring");

const YOUR_API_KEY = "<YOUR_API_KEY>";
const CONNECTION_PARAMS = { sample_rate: 16000 };
const API_ENDPOINT_BASE_URL = "wss://streaming.eu.assemblyai.com/v3/ws";
const API_ENDPOINT = `${API_ENDPOINT_BASE_URL}?${querystring.stringify(CONNECTION_PARAMS)}`;

const ws = new WebSocket(API_ENDPOINT, {
  headers: {
    Authorization: YOUR_API_KEY,
  },
});
