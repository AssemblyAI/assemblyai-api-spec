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
