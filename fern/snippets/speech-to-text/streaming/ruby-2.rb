list = ["aws", "azure", "google cloud"]
word_boost = URI.encode_www_form_component(JSON.dump(list))

ws = WebSocket::Client::Simple.connect(
  "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=#{SAMPLE_RATE}&word_boost=#{word_boost}",
  ...
)
