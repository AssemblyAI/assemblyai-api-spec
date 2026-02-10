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
