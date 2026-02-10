ws.on("close", (code, reason) => onClose(ws, code, reason));

function onClose(ws, code, reason) {
  if (recording) {
    recording.end();
  }
  console.log("Disconnected");
}

process.on("SIGINT", async function () {
  console.log();
  console.log("Stopping recording");
  if (recording) {
    recording.end();
  }
  console.log("Closing real-time transcript connection");
  if (ws.readyState === WebSocket.OPEN) {
    ws.close();
  }
  process.exit();
});
