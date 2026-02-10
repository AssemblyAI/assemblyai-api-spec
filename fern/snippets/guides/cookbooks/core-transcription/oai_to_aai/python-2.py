import assemblyai as aai

aai.settings.api_key = "YOUR-API-KEY"
transcriber = aai.Transcriber()

audio_file = "./example.wav"

transcript = transcriber.transcribe(audio_file)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
    exit(1)

print(transcript.text)
