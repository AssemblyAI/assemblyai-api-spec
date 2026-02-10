config = aai.TranscriptionConfig(
    speaker_labels=True,  # Speaker diarization
    filter_profanity=True,  # Remove profanity from transcript
    speakers_expected:2  # Specify amount of speakers in audio
)

transcript = transcriber.transcribe(audio_file, config)

# Access speaker labels

for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")
