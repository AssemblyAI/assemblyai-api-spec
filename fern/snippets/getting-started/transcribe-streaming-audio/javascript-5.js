async function run() {
  console.log("Starting AssemblyAI streaming transcription...");
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
