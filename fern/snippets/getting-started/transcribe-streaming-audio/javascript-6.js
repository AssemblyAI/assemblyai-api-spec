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
