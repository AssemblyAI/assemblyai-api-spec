config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=8000,
    language_code="en-US",
    enable_speaker_diarization=True,  # Speaker diarization
    diarization_speaker_count=2,  # Specify amount of speakers
    profanity_filter=True   # Remove profanity from transcript
)
