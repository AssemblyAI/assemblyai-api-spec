# Define a callback to handle the session information message
if msg_type == 'SessionInformation':
    audio_duration_seconds = msg.get('audio_duration_seconds')
    print(f"Audio duration: {audio_duration_seconds}")

# Configure the on_extra_session_information parameter
ws = websocket.WebSocketApp(
    f'wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}&enable_extra_session_information=true',
    ...,
)
