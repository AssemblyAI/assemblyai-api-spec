def run_streaming(config):
    global audio, stream, ws_app, OPTIMIZED_CONFIG

    OPTIMIZED_CONFIG = config

    print("\n" + "=" * 70)
    print("STARTING REAL-TIME STREAMING")
    print("=" * 70)

    # Build connection parameters with optimized settings
    CONNECTION_PARAMS = {
        "sample_rate": SAMPLE_RATE,
        "format_turns": True,
        "end_of_turn_confidence_threshold": config['end_of_turn_confidence_threshold'],
        "min_end_of_turn_silence_when_confident": str(config['min_end_of_turn_silence_when_confident']),
        "max_turn_silence": str(config['max_turn_silence'])
    }

    API_ENDPOINT_BASE_URL = "wss://streaming.assemblyai.com/v3/ws"
    API_ENDPOINT = f"{API_ENDPOINT_BASE_URL}?{urlencode(CONNECTION_PARAMS)}"

    print(f"\nWebSocket Endpoint: {API_ENDPOINT_BASE_URL}")
    print(f"\nApplied Configuration:")
    for key, value in CONNECTION_PARAMS.items():
        print(f"   • {key}: {value}")

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open microphone stream
    try:
        stream = audio.open(
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            channels=CHANNELS,
            format=FORMAT,
            rate=SAMPLE_RATE,
        )
        print("\nMicrophone stream opened successfully.")
    except Exception as e:
        print(f"Error opening microphone stream: {e}")
        if audio:
            audio.terminate()
        return

    # Create WebSocketApp
    ws_app = websocket.WebSocketApp(
        API_ENDPOINT,
        header={"Authorization": YOUR_API_KEY},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Run WebSocketApp in a separate thread
    ws_thread = threading.Thread(target=ws_app.run_forever)
    ws_thread.daemon = True
    ws_thread.start()

    try:
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nCtrl+C received. Stopping...")
        stop_event.set()

        if ws_app and ws_app.sock and ws_app.sock.connected:
            try:
                terminate_message = {"type": "Terminate"}
                print(f"Sending termination message...")
                ws_app.send(json.dumps(terminate_message))
                time.sleep(1)
            except Exception as e:
                print(f"Error sending termination message: {e}")

        if ws_app:
            ws_app.close()

        ws_thread.join(timeout=2.0)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        stop_event.set()
        if ws_app:
            ws_app.close()
        ws_thread.join(timeout=2.0)

    finally:
        if stream and stream.is_active():
            stream.stop_stream()
        if stream:
            stream.close()
        if audio:
            audio.terminate()
        print("Cleanup complete. Exiting.")
