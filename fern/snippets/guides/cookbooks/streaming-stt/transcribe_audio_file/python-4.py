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
