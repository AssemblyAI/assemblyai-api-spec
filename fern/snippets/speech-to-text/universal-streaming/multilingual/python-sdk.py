import logging
from typing import Type

import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent,
)

api_key = "<YOUR_API_KEY>"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_begin(self: Type[StreamingClient], event: BeginEvent):
    print(f"Connecting websocket to url")
    print(f"Session started: {event.id}")
    print(f"Receiving SessionBegins ...")
    print(f"Sending messages ...")


def on_turn(self: Type[StreamingClient], event: TurnEvent):
    if not event.end_of_turn and event.transcript:
        print(f"[PARTIAL TURN TRANSCRIPT]: {event.transcript}")
    if event.utterance:
        print(f"[PARTIAL TURN UTTERANCE]: {event.utterance}")
        # Display language detection info if available
        if event.language_code:
            print(f"[UTTERANCE LANGUAGE DETECTION]: {event.language_code} - {event.language_confidence:.2%}")
    if event.end_of_turn:
        print(f"[FULL TURN TRANSCRIPT]: {event.transcript}")
        # Display language detection info if available
        if event.language_code:
            print(f"[END OF TURN LANGUAGE DETECTION]: {event.language_code} - {event.language_confidence:.2%}")


def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
    print(
        f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
    )


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
            sample_rate=48000,
            speech_model="universal-streaming-multilingual",
            language_detection=True,
        )
    )

    try:
        client.stream(
          aai.extras.MicrophoneStream(sample_rate=48000)
        )
    finally:
        client.disconnect(terminate=True)


if __name__ == "__main__":
    main()
