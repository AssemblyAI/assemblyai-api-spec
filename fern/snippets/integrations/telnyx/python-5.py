serializer = TelnyxFrameSerializer(
    stream_id=stream_id,
    call_control_id=call_control_id,
    api_key=os.getenv("TELNYX_API_KEY"),  # Enables auto-termination
)
