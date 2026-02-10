data = {
    "audio_url": upload_url,
    "diarization": True,                # Speaker diarization
    "chapterization": True,             # Auto chapter detection
    "named_entity_recognition": True    # Named entity detection
}

# Access speaker labels
for utterance in transcript['result']['transcription']['utterances']:
    print(f"Speaker {utterance['speaker']}: {utterance['text']}")

# Access auto chapters
for chapter in transcript['result']['chapterization']['results']:
    print(f"{chapter['start']} - {chapter['end']}: {chapter['headline']}")

# Access named entities
for entity in transcript['result']['named_entity_recognition']['results']:
    print(entity['text'])
    print(entity['entity_type'])
    print(f"Timestamp: {entity['start']} - {entity['end']}\n")
