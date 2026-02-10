// Define a callback to handle the session information message
if (msgType === 'SessionInformation') {
      const audioDurationSeconds = msg.audio_duration_seconds;
      console.log(`Audio duration: ${audioDurationSeconds}`);
    }

// Configure the on_extra_session_information parameter
const ws = new WebSocket(
    `wss://api.assemblyai.com/v2/realtime/ws?sample_rate=${SAMPLE_RATE}&enable_extra_session_information=true`,
    ...,
  );
