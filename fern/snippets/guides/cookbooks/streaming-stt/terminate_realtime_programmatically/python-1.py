import logging
from datetime import datetime
from typing import Type

import assemblyai as aai
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

api_key = "<YOUR_API_KEY>"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

last_transcript_received = datetime.now()
terminated = False


def on_begin(self: Type[StreamingClient], event: BeginEvent):
    print(f"Session started: {event.id}")


def on_turn(self: Type[StreamingClient], event: TurnEvent):
    global last_transcript_received, terminated

    if terminated:
        return

    print(f"{event.transcript} ({event.end_of_turn})")

    if event.transcript.strip():
        last_transcript_received = datetime.now()

    silence_duration = (datetime.now() - last_transcript_received).total_seconds()
    if silence_duration > 5:
        print("No transcription received in 5 seconds. Terminating session...")
        self.disconnect(terminate=True)
        terminated = True
        return

    if event.end_of_turn and not event.turn_is_formatted:
        self.set_params(StreamingSessionParameters(format_turns=True))


def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
    print(f"Session terminated after {event.audio_duration_seconds:.2f} seconds")


def on_error(self: Type[StreamingClient], error: StreamingError):
    print(f"Error occurred: {error}")


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
        client.stream(aai.extras.MicrophoneStream(sample_rate=16000))
    finally:
        if not terminated:
            client.disconnect(terminate=True)


if __name__ == "__main__":
    main()
