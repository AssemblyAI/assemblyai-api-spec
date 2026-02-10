ws = websocket.WebSocketApp(
    f'wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}',
    header={'Authorization': YOUR_API_KEY},
    on_message=on_message,
    on_open=on_open,
    on_error=on_error,
    on_close=on_close
)
