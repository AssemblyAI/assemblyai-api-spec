data = {
    "audio_url": upload_url,
    "speaker_labels": True,     # Speaker diarization
    "auto_chapters": True,      # Auto chapter detection
    "entity_detection": True    # Named entity detection
}

# Access speaker labels
for utterance in transcript['utterances']:
    print(f"Speaker {utterance['speaker']}: {utterance['text']}")

# Access auto chapters
for chapter in transcript['chapters']:
    print(f"{chapter['start']} - {chapter['end']}: {chapter['headline']}")

# Access named entities
for entity in transcript['entities']:
    print(entity['text'])
    print(entity['entity_type'])
    print(f"Timestamp: {entity['start']} - {entity['end']}\n")
