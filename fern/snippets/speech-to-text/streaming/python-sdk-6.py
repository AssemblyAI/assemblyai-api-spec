# Define a callback to handle the session information message
def on_extra_session_information(data: aai.RealtimeSessionInformation):
    print(data.audio_duration_seconds)

# Configure the RealtimeTranscriber
transcriber = aai.RealtimeTranscriber(
    ...,
    on_extra_session_information=on_extra_session_information,
)
