import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent
)
from typing import Type
import sys

YOUR_API_KEY = "YOUR_API_KEY"  # Replace with your AssemblyAI API key
AUDIO_FILE = "audio.wav"  # Path to your audio file
SAMPLE_RATE = 48000  # Change to match the sample rate of your audio file
SAVE_TRANSCRIPT_TO_FILE = True  # Set to False to disable saving transcript to file
PLAY_AUDIO = True  # Set to False to disable audio playback

# Track session data for output file
session_data = {
    "session_id": None,
    "parameters": None,
    "audio_file": AUDIO_FILE,
    "audio_duration_seconds": None,
    "turns": []
}

def on_begin(self: Type[StreamingClient], event: BeginEvent):
  "This function is called when the connection has been established."

  session_data["session_id"] = event.id
  print("Session ID:", event.id, "\n")

def on_turn(self: Type[StreamingClient], event: TurnEvent):
  "This function is called when a new transcript has been received."

  # Skip empty transcripts
  if not event.transcript:
    return

  # Determine status label
  if not event.end_of_turn:
    status = "[Partial]"
  elif event.turn_is_formatted:
    status = "[Final (formatted)]"
  else:
    status = "[Final (unformatted)]"

  print(f"{status}: {event.transcript}")

  # Track final turns (formatted if formatting is enabled, otherwise just final)
  is_final = event.end_of_turn and (not streaming_params.format_turns or event.turn_is_formatted)
  if is_final:
    session_data["turns"].append(event.transcript)
    print()  # Add blank line after final formatted turn for cleaner output

def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
  "This function is called when the session has ended."

  session_data["audio_duration_seconds"] = event.audio_duration_seconds
  print(
    f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
  )

def on_error(self: Type[StreamingClient], error: StreamingError):
  "This function is called when an error occurs."

  print(f"Error occurred: {error}")

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


# Create the streaming client
client = StreamingClient(
  StreamingClientOptions(
    api_key=YOUR_API_KEY
  )
)

client.on(StreamingEvents.Begin, on_begin)
client.on(StreamingEvents.Turn, on_turn)
client.on(StreamingEvents.Termination, on_terminated)
client.on(StreamingEvents.Error, on_error)

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

# Configure streaming parameters
streaming_params = StreamingParameters(
    sample_rate=SAMPLE_RATE,
    format_turns=True,
    speech_model="universal-streaming-english",
)

# Store parameters for output file (dynamically capture all set parameters)
session_data["parameters"] = ", ".join(
    f"{k}={v}" for k, v in streaming_params.__dict__.items() if v is not None
)

# Warn if using default turn detection parameters
turn_params = ["end_of_turn_confidence_threshold", "min_end_of_turn_silence_when_confident", "max_turn_silence"]
if not any(getattr(streaming_params, p, None) is not None for p in turn_params):
    print("Warning: Using default turn detection parameters. For best results, fine-tune to your use case:")
    print("https://www.assemblyai.com/docs/universal-streaming/turn-detection#quick-start-configurations\n")

client.connect(streaming_params)

try:
    client.stream(file_stream)
finally:
    client.disconnect(terminate=True)
    if SAVE_TRANSCRIPT_TO_FILE:
        save_transcript()
