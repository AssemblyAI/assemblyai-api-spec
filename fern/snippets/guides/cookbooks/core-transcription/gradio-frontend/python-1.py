import assemblyai

# Set your API key here, which can be found on your Dashboard as mentioned above.
assemblyai.settings.api_key = "API_KEY_HERE"


def transcribe(audio_path):
    transcriber = assemblyai.Transcriber()
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == assemblyai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
