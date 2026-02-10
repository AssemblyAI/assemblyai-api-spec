config = aai.TranscriptionConfig(
    speaker_labels=True,           # Speaker diarization
    auto_chapters=True,           # Auto chapter detection
    entity_detection=True,        # Named entity detection
)

transcript = transcriber.transcribe(audio_file, config)

# Access speaker labels

for utterance in transcript.utterances:
print(f"Speaker {utterance.speaker}: {utterance.text}")
