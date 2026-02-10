def on_open(ws):
    def stream_audio():
        while True:
            try:
                audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
            except Exception as e:
                print(f'\nError streaming audio: {e}')
                break

    audio_thread = Thread(target=stream_audio, daemon=True)
    audio_thread.start()
