ws.on("message", (message) => {
  try {
    const msg = JSON.parse(message);
    const msgType = msg.message_type;

    if (msgType === "SessionBegins") {
      const sessionId = msg.session_id;
      console.log("Session ID:", sessionId);
      return;
    }

    const text = msg.text || "";
    if (!text) {
      return;
    }

    if (msgType === "PartialTranscript") {
      console.log("Partial:", text);
    } else if (msgType === "FinalTranscript") {
      console.log("Final:", text);
    } else if (msgType === "error") {
      console.error("Error:", msg.error);
    }
  } catch (error) {
    console.error("Error handling message:", error);
  }
});
