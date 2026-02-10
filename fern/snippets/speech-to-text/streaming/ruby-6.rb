# Define a callback to handle the session information message
if msg_type == 'SessionInformation'
      audio_duration_seconds = msg['audio_duration_seconds']
      puts "Audio duration: #{audio_duration_seconds}"
      return
    end

# Configure the on_extra_session_information parameter
ws = WebSocket::Client::Simple.connect(
  "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=#{SAMPLE_RATE}&on_extra_session_information=true",
  ...
)
