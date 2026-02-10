def save_transcript():
  "Save the transcript to a file in the same directory as the script."
  from pathlib import Path

  # Get the audio file name (handles both absolute and relative paths)
  audio_name = Path(session_data["audio_file"]).stem

  # Generate filename: {file_name}_{session_id}.txt in the same directory as script
  session_id = session_data["session_id"] or "unknown"
  output_file = f"{audio_name}_{session_id}.txt"

  with open(output_file, "w") as f:
    f.write(f"AssemblyAI Session ID: {session_data['session_id']}\n")
    f.write(f"Audio file: {session_data['audio_file']}\n")
    f.write(f"Audio duration: {session_data['audio_duration_seconds']} seconds\n")
    f.write(f"Parameters used: {session_data['parameters']}\n")
    f.write("See all available parameters and defaults at https://www.assemblyai.com/docs/api-reference/streaming-api/streaming-api#request.query\n\n")

    f.write("\nTranscription Output\n")
    for i, turn in enumerate(session_data["turns"], 1):
      f.write(f"[Turn #{i}]: {turn}\n")

  print(f"Transcript saved to {output_file}")

def validate_audio_file(filepath: str, sample_rate: int):
    """Validate audio file before streaming"""
    import wave
    from pathlib import Path

    # Check file extension
    file_ext = Path(filepath).suffix.lower()
    if file_ext != ".wav":
        print(f"Error: Only WAV files are supported. Got: {file_ext}", file=sys.stderr)
        print(f"Convert your file to WAV using: ffmpeg -i {filepath} -ar {sample_rate} -ac 1 output.wav", file=sys.stderr)
        sys.exit(1)

    with wave.open(filepath, 'rb') as wav_file:
        if wav_file.getnchannels() != 1:
            print("Error: Only mono audio is supported", file=sys.stderr)
            print(f"Convert your file to mono using: ffmpeg -i {filepath} -ar {sample_rate} -ac 1 output.wav", file=sys.stderr)
            sys.exit(1)

        file_sample_rate = wav_file.getframerate()
        if file_sample_rate != sample_rate:
            print(f"Error: File sample rate ({file_sample_rate}) doesn't match expected rate ({sample_rate})", file=sys.stderr)
            print(f"Either update SAMPLE_RATE to {file_sample_rate}, or convert your file using: ffmpeg -i {filepath} -ar {sample_rate} -ac 1 output.wav", file=sys.stderr)
            sys.exit(1)

def stream_file(filepath: str, sample_rate: int, play_audio: bool = False):
    """Stream audio file in 50ms chunks, optionally playing audio"""
    import time
    import wave

    chunk_duration = 0.05
    audio_player = None

    if play_audio:
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            with wave.open(filepath, 'rb') as wav_file:
                audio_player = p.open(
                    format=p.get_format_from_width(wav_file.getsampwidth()),
                    channels=wav_file.getnchannels(),
                    rate=wav_file.getframerate(),
                    output=True
                )
        except ImportError:
            print("Warning: pyaudio not installed. Audio playback disabled.", file=sys.stderr)
            print("Install with: pip install pyaudio", file=sys.stderr)
            play_audio = False

    try:
        with wave.open(filepath, 'rb') as wav_file:
            frames_per_chunk = int(sample_rate * chunk_duration)

            while True:
                frames = wav_file.readframes(frames_per_chunk)

                if not frames:
                    break

                if audio_player:
                    audio_player.write(frames)
                else:
                    time.sleep(chunk_duration)

                yield frames
    finally:
        if audio_player:
            audio_player.stop_stream()
            audio_player.close()
            p.terminate()

# Validate audio file before connecting
validate_audio_file(AUDIO_FILE, SAMPLE_RATE)

file_stream = stream_file(
  filepath=AUDIO_FILE,
  sample_rate=SAMPLE_RATE,
  play_audio=PLAY_AUDIO,
)
