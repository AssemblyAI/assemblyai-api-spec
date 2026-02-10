list = ["aws", "azure", "google cloud"]
word_boost = urllib.parse.quote(json.dumps(list))
ws = websocket.WebSocketApp(
    f'wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}&encoding=pcm_mulaw&word_boost={word_boost}',
    ...,
)
