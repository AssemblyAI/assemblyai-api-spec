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
