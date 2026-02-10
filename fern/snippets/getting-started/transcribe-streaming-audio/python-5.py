# --- WebSocket Event Handlers ---
def on_open(ws):
    """Called when the WebSocket connection is established."""
    print("WebSocket connection opened.")
    print(f"Connected to: {API_ENDPOINT}")
    # Start sending audio data in a separate thread
    def stream_audio():
        global stream
        print("Starting audio streaming...")
        while not stop_event.is_set():
            try:
                audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)

                # Store audio data for WAV recording
                with recording_lock:
                    recorded_frames.append(audio_data)

                # Send audio data as binary message
                ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
            except Exception as e:
                print(f"Error streaming audio: {e}")
                # If stream read fails, likely means it's closed, stop the loop
                break
        print("Audio streaming stopped.")
    global audio_thread
    audio_thread = threading.Thread(target=stream_audio)
    audio_thread.daemon = (
        True  # Allow main thread to exit even if this thread is running
    )
    audio_thread.start()
def on_message(ws, message):
    try:
        data = json.loads(message)
        msg_type = data.get('type')
        if msg_type == "Begin":
            session_id = data.get('id')
            expires_at = data.get('expires_at')
            print(f"\nSession began: ID={session_id}, ExpiresAt={datetime.fromtimestamp(expires_at)}")
        elif msg_type == "Turn":
            transcript = data.get('transcript', '')
            formatted = data.get('turn_is_formatted', False)
            # Clear previous line for formatted messages
            if formatted:
                print('\r' + ' ' * 80 + '\r', end='')
                print(transcript)
            else:
                print(f"\r{transcript}", end='')
        elif msg_type == "Termination":
            audio_duration = data.get('audio_duration_seconds', 0)
            session_duration = data.get('session_duration_seconds', 0)
            print(f"\nSession Terminated: Audio Duration={audio_duration}s, Session Duration={session_duration}s")
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")
def on_error(ws, error):
    """Called when a WebSocket error occurs."""
    print(f"\nWebSocket Error: {error}")
    # Attempt to signal stop on error
    stop_event.set()
def on_close(ws, close_status_code, close_msg):
    """Called when the WebSocket connection is closed."""
    print(f"\nWebSocket Disconnected: Status={close_status_code}, Msg={close_msg}")

    # Save recorded audio to WAV file
    save_wav_file()

    # Ensure audio resources are released
    global stream, audio
    stop_event.set()  # Signal audio thread just in case it's still running
    if stream:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        stream = None
    if audio:
        audio.terminate()
        audio = None
    # Try to join the audio thread to ensure clean exit
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=1.0)
