def display_transcript(transcript_data):
    for clip_index, utterances in transcript_data.items():
        print(f"Clip {clip_index + 1}:")
        for utterance in utterances:
            speaker = utterance['speaker']
            text = utterance['text']
            print(f"  Speaker {speaker}: {text}")
        print("\n")  # Add an extra newline for spacing between


display_transcript(clip_utterances)
