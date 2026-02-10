config = aai.TranscriptionConfig(
    language_code = "en" # Set language code
    speaker_labels = True, # Speaker diarization
    sentiment_analysis=True, # Sentiment Analysis
    entity_detection = True, # Named entity detection
)

transcript = transcriber.transcribe(audio_url, config)

# Access word-level timestamps
print(transcript.words)

# Access speaker labels
for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")
