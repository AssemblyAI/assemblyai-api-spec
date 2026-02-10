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
