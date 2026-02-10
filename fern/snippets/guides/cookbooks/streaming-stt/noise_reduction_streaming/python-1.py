import logging
import numpy as np
import noisereduce as nr
import assemblyai as aai
from typing import Type
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    StreamingSessionParameters,
    TerminationEvent,
    TurnEvent,
)

logging.basicConfig(level=logging.INFO)

api_key = "<YOUR_API_KEY>"

# --- Noise-reduced microphone stream ---
def noise_reduced_mic_stream(sample_rate=16000):
    mic = aai.extras.MicrophoneStream(sample_rate=sample_rate)
    buffer = np.array([], dtype=np.int16)
    buffer_size = int(sample_rate * 0.5)  # 0.5 seconds

    for raw_audio in mic:
        audio_data = np.frombuffer(raw_audio, dtype=np.int16)
        buffer = np.append(buffer, audio_data)

        if len(buffer) >= buffer_size:
            float_audio = buffer.astype(np.float32) / 32768.0
            denoised = nr.reduce_noise(
                y=float_audio,
                sr=sample_rate,
                prop_decrease=0.75,
                n_fft=1024,
            )
            int_audio = (denoised * 32768.0).astype(np.int16)
            buffer = buffer[-1024:]  # keep some overlap
            yield int_audio.tobytes()


# --- Event Handlers ---
def on_begin(self: Type[StreamingClient], event: BeginEvent):
    print(f" Session started: {event.id}")

def on_turn(self: Type[StreamingClient], event: TurnEvent):
    print(f"{event.transcript} ({event.end_of_turn})")

    if event.end_of_turn and not event.turn_is_formatted:
        self.set_params(StreamingSessionParameters(format_turns=True))

def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
    print(f" Session terminated after {event.audio_duration_seconds} seconds")

def on_error(self: Type[StreamingClient], error: StreamingError):
    print(f" Error occurred: {error}")

# --- Main Function ---
def main():
    client = StreamingClient(
        StreamingClientOptions(
            api_key=api_key,
            api_host="streaming.assemblyai.com",
        )
    )

    client.on(StreamingEvents.Begin, on_begin)
    client.on(StreamingEvents.Turn, on_turn)
    client.on(StreamingEvents.Termination, on_terminated)
    client.on(StreamingEvents.Error, on_error)

    client.connect(
        StreamingParameters(
            sample_rate=16000,
            format_turns=True,
        )
    )

    try:
        denoised_stream = noise_reduced_mic_stream(sample_rate=16000)
        client.stream(denoised_stream)
    finally:
        client.disconnect(terminate=True)

if __name__ == "__main__":
    main()
