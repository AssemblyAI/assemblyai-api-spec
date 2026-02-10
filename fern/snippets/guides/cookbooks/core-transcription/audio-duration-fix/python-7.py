def transcribe(file):
    print("Executing transcription as audio durations are consistent.")
    transcript = transcriber.transcribe(file)
    print(transcript.text)
