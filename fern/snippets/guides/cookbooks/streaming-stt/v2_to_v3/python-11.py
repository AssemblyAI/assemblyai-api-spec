def on_close(ws, close_status_code, close_msg):
    print(f"\nWebSocket Disconnected: Status={close_status_code}, Msg={close_msg}")
    global stream, audio
    stop_event.set()  # Signal audio thread to stop

    if stream:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        stream = None
    if audio:
        audio.terminate()
        audio = None
    # Ensure audio thread cleanup
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=1.0)

def on_error(ws, error):
    print(f"\nWebSocket Error: {error}")
    stop_event.set()  # Signal threads to stop on error
