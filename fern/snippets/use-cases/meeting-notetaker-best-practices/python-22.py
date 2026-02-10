def process_async_transcript(transcript):
    """
    Extract and process all relevant data from async transcript
    """
    # Basic transcript data
    meeting_data = {
        "id": transcript.id,
        "duration": transcript.audio_duration,
        "confidence": transcript.confidence,
        "full_text": transcript.text
    }

    # Process speaker utterances
    speakers = {}
    for utterance in transcript.utterances:
        speaker = utterance.speaker

        if speaker not in speakers:
            speakers[speaker] = {
                "utterances": [],
                "total_speaking_time": 0,
                "word_count": 0
            }

        speakers[speaker]["utterances"].append({
            "text": utterance.text,
            "start": utterance.start,
            "end": utterance.end,
            "confidence": utterance.confidence
        })

        # Calculate speaking time
        speakers[speaker]["total_speaking_time"] += (utterance.end - utterance.start) / 1000
        speakers[speaker]["word_count"] += len(utterance.text.split())

    meeting_data["speakers"] = speakers

    # Extract summary
    if transcript.summary:
        meeting_data["summary"] = transcript.summary

    # Calculate meeting statistics
    total_duration = transcript.audio_duration / 1000  # Convert to seconds
    meeting_data["statistics"] = {
        "total_speakers": len(speakers),
        "total_words": sum(s["word_count"] for s in speakers.values()),
        "average_confidence": transcript.confidence,
        "speaking_distribution": {
            speaker: {
                "percentage": (data["total_speaking_time"] / total_duration) * 100,
                "minutes": data["total_speaking_time"] / 60
            }
            for speaker, data in speakers.items()
        }
    }

    return meeting_data

# Example usage
result = process_async_transcript(transcript)
print(f"Meeting had {result['statistics']['total_speakers']} speakers")
print(f"Speaker A spoke for {result['statistics']['speaking_distribution']['A']['minutes']:.1f} minutes")
