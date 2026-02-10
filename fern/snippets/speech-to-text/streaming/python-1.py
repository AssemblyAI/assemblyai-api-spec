ws = websocket.WebSocketApp(
    f'wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}&encoding=pcm_mulaw',
    ...,
)
