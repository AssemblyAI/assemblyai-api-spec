ws = WebSocket::Client::Simple.connect(
  "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=#{SAMPLE_RATE}&token=#{token}",
  ...
)
