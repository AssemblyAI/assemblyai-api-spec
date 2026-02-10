if transcript.error:
    if "below the requested confidence threshold value" in transcript.error:
        print(f"{transcript.error}. Running transcript again with language set to '{default_language}'.")
        new_config = aai.TranscriptionConfig(language_code=default_language)
        transcript = transcriber.transcribe(audio_url, new_config)
        print(f"Transcript ID: {transcript.id}")
        print(transcript.text)
    else:
        print(transcript.error)
else:
    print(f"Transcript ID: {transcript.id}")
    print(transcript.text)
