config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True,
    speaker_labels=True,
)

transcript = aai.Transcriber().transcribe(audio_file, config=config)
