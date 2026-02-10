def on_begin(self: Type[StreamingClient], event: BeginEvent):
  "This function is called when the connection has been established."

  print("Session ID:", event.id)

def on_turn(self: Type[StreamingClient], event: TurnEvent):
  "This function is called when a new transcript has been received."
  global assembly_streaming_transcript

  if event.end_of_turn and event.turn_is_formatted:
    assembly_streaming_transcript += event.transcript + " "

  print(event.transcript, end="\r\n")

def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
  "This function is called when an error occurs."

  print(
    f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
  )

def on_error(self: Type[StreamingClient], error: StreamingError):
  "This function is called when the connection has been closed."

  print(f"Error occurred: {error}")


# Create the streaming client
client = StreamingClient(
  StreamingClientOptions(
    api_key="YOUR-API-KEY"
  )
)

client.on(StreamingEvents.Begin, on_begin)
client.on(StreamingEvents.Turn, on_turn)
client.on(StreamingEvents.Termination, on_terminated)
client.on(StreamingEvents.Error, on_error)

def stream_file(filepath: str, sample_rate: int):
    """Stream audio file in 50ms chunks instead of 300ms"""
    import time
    import wave

    chunk_duration = 0.1

    with wave.open(filepath, 'rb') as wav_file:
        if wav_file.getnchannels() != 1:
            raise ValueError("Only mono audio is supported")

        file_sample_rate = wav_file.getframerate()
        if file_sample_rate != sample_rate:
            print(f"Warning: File sample rate ({file_sample_rate}) doesn't match expected rate ({sample_rate})")

        frames_per_chunk = int(file_sample_rate * chunk_duration)

        while True:
            frames = wav_file.readframes(frames_per_chunk)

            if not frames:
                break

            yield frames

            # time.sleep(chunk_duration)

file_stream = stream_file(
  filepath="audio.wav",
  sample_rate=48000,
)

client.connect(
    StreamingParameters(
        sample_rate=48000,
        format_turns=True,
    )
)

try:
    client.stream(file_stream)
finally:
    client.disconnect(terminate=True)
