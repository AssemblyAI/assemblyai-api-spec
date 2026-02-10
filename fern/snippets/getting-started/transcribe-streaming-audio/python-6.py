def run():
    global audio, stream, ws_app
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
        print("Microphone stream opened successfully.")
        print("Speak into your microphone. Press Ctrl+C to stop.")
        print("Audio will be saved to a WAV file when the session ends.")
    except Exception as e:
        print(f"Error opening microphone stream: {e}")
        if audio:
            audio.terminate()
        return  # Exit if microphone cannot be opened
