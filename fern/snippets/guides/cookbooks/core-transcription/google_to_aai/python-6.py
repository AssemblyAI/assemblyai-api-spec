transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_file)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
else:
    print(transcript.text)
