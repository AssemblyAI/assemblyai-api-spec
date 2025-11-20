const WebSocket = require("ws");
const mic = require("mic");
const querystring = require("querystring");
const fs = require("fs");

// --- Configuration ---
const YOUR_API_KEY = "YOUR-API-KEY"; // Replace with your actual API key
const CONNECTION_PARAMS = {
  sample_rate: 16000,
  format_turns: true, // Request formatted final transcripts
  speech_model: "universal-streaming-multilingual"
};
const API_ENDPOINT_BASE_URL = "wss://streaming.assemblyai.com/v3/ws";
const API_ENDPOINT = `${API_ENDPOINT_BASE_URL}?${querystring.stringify(CONNECTION_PARAMS)}`;

// Audio Configuration
const SAMPLE_RATE = CONNECTION_PARAMS.sample_rate;
const CHANNELS = 1;

// Global variables
let micInstance = null;
let micInputStream = null;
let ws = null;
let stopRequested = false;

// WAV recording variables
let recordedFrames = []; // Store audio frames for WAV file

// --- Helper functions ---
function clearLine() {
  process.stdout.write("\r" + " ".repeat(80) + "\r");
}

function formatTimestamp(timestamp) {
  return new Date(timestamp * 1000).toISOString();
}

function createWavHeader(sampleRate, channels, dataLength) {
  const buffer = Buffer.alloc(44);

  // RIFF header
  buffer.write("RIFF", 0);
  buffer.writeUInt32LE(36 + dataLength, 4);
  buffer.write("WAVE", 8);

  // fmt chunk
  buffer.write("fmt ", 12);
  buffer.writeUInt32LE(16, 16); // fmt chunk size
  buffer.writeUInt16LE(1, 20); // PCM format
  buffer.writeUInt16LE(channels, 22);
  buffer.writeUInt32LE(sampleRate, 24);
  buffer.writeUInt32LE(sampleRate * channels * 2, 28); // byte rate
  buffer.writeUInt16LE(channels * 2, 32); // block align
  buffer.writeUInt16LE(16, 34); // bits per sample

  // data chunk
  buffer.write("data", 36);
  buffer.writeUInt32LE(dataLength, 40);

  return buffer;
}

function saveWavFile() {
  if (recordedFrames.length === 0) {
    console.log("No audio data recorded.");
    return;
  }

  // Generate filename with timestamp
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const filename = `recorded_audio_${timestamp}.wav`;

  try {
    // Combine all recorded frames
    const audioData = Buffer.concat(recordedFrames);
    const dataLength = audioData.length;

    // Create WAV header
    const wavHeader = createWavHeader(SAMPLE_RATE, CHANNELS, dataLength);

    // Write WAV file
    const wavFile = Buffer.concat([wavHeader, audioData]);
    fs.writeFileSync(filename, wavFile);

    console.log(`Audio saved to: ${filename}`);
    console.log(
      `Duration: ${(dataLength / (SAMPLE_RATE * CHANNELS * 2)).toFixed(2)} seconds`
    );
  } catch (error) {
    console.error(`Error saving WAV file: ${error}`);
  }
}

// --- Main function ---
async function run() {
  console.log("Starting AssemblyAI real-time transcription...");
  console.log("Audio will be saved to a WAV file when the session ends.");

  // Initialize WebSocket connection
  ws = new WebSocket(API_ENDPOINT, {
    headers: {
      Authorization: YOUR_API_KEY,
    },
  });

  // Setup WebSocket event handlers
  ws.on("open", () => {
    console.log("WebSocket connection opened.");
    console.log(`Connected to: ${API_ENDPOINT}`);
    // Start the microphone
    startMicrophone();
  });

  ws.on("message", (message) => {
    try {
      const data = JSON.parse(message);
      const msgType = data.type;

      if (msgType === "Begin") {
        const sessionId = data.id;
        const expiresAt = data.expires_at;
        console.log(
          `\nSession began: ID=${sessionId}, ExpiresAt=${formatTimestamp(expiresAt)}`
        );
      } else if (msgType === "Turn") {
        const transcript = data.transcript || "";
        const formatted = data.turn_is_formatted;

        if (formatted) {
          clearLine();
          console.log(transcript);
        } else {
          process.stdout.write(`\r${transcript}`);
        }
      } else if (msgType === "Termination") {
        const audioDuration = data.audio_duration_seconds;
        const sessionDuration = data.session_duration_seconds;
        console.log(
          `\nSession Terminated: Audio Duration=${audioDuration}s, Session Duration=${sessionDuration}s`
        );
      }
    } catch (error) {
      console.error(`\nError handling message: ${error}`);
      console.error(`Message data: ${message}`);
    }
  });

  ws.on("error", (error) => {
    console.error(`\nWebSocket Error: ${error}`);
    cleanup();
  });

  ws.on("close", (code, reason) => {
    console.log(`\nWebSocket Disconnected: Status=${code}, Msg=${reason}`);
    cleanup();
  });

  // Handle process termination
  setupTerminationHandlers();
}

function startMicrophone() {
  try {
    micInstance = mic({
      rate: SAMPLE_RATE.toString(),
      channels: CHANNELS.toString(),
      debug: false,
      exitOnSilence: 6, // This won't actually exit, just a parameter for mic
    });

    micInputStream = micInstance.getAudioStream();

    micInputStream.on("data", (data) => {
      if (ws && ws.readyState === WebSocket.OPEN && !stopRequested) {
        // Store audio data for WAV recording
        recordedFrames.push(Buffer.from(data));

        // Send audio data to WebSocket
        ws.send(data);
      }
    });

    micInputStream.on("error", (err) => {
      console.error(`Microphone Error: ${err}`);
      cleanup();
    });

    micInstance.start();
    console.log("Microphone stream opened successfully.");
    console.log("Speak into your microphone. Press Ctrl+C to stop.");
  } catch (error) {
    console.error(`Error opening microphone stream: ${error}`);
    cleanup();
  }
}

function cleanup() {
  stopRequested = true;

  // Save recorded audio to WAV file
  saveWavFile();

  // Stop microphone if it's running
  if (micInstance) {
    try {
      micInstance.stop();
    } catch (error) {
      console.error(`Error stopping microphone: ${error}`);
    }
    micInstance = null;
  }

  // Close WebSocket connection if it's open
  if (ws && [WebSocket.OPEN, WebSocket.CONNECTING].includes(ws.readyState)) {
    try {
      // Send termination message if possible
      if (ws.readyState === WebSocket.OPEN) {
        const terminateMessage = { type: "Terminate" };
        console.log(
          `Sending termination message: ${JSON.stringify(terminateMessage)}`
        );
        ws.send(JSON.stringify(terminateMessage));
      }
      ws.close();
    } catch (error) {
      console.error(`Error closing WebSocket: ${error}`);
    }
    ws = null;
  }

  console.log("Cleanup complete.");
}

function setupTerminationHandlers() {
  // Handle Ctrl+C and other termination signals
  process.on("SIGINT", () => {
    console.log("\nCtrl+C received. Stopping...");
    cleanup();
    // Give time for cleanup before exiting
    setTimeout(() => process.exit(0), 1000);
  });

  process.on("SIGTERM", () => {
    console.log("\nTermination signal received. Stopping...");
    cleanup();
    // Give time for cleanup before exiting
    setTimeout(() => process.exit(0), 1000);
  });

  // Handle uncaught exceptions
  process.on("uncaughtException", (error) => {
    console.error(`\nUncaught exception: ${error}`);
    cleanup();
    // Give time for cleanup before exiting
    setTimeout(() => process.exit(1), 1000);
  });
}

// Start the application
run();