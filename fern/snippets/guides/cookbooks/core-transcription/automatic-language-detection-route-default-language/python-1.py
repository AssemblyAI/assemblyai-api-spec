transcriber = aai.Transcriber()
audio_url = ("https://example.org/audio.mp3")
config = aai.TranscriptionConfig(language_detection=True, language_confidence_threshold=0.8)
transcript = transcriber.transcribe(audio_url, config)
