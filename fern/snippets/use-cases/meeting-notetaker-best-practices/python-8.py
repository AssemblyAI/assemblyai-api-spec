import assemblyai as aai

aai.settings.api_key = "your_api_key"

# Step 1: Transcribe with speaker diarization
config = aai.TranscriptionConfig(
    speaker_labels=True,  # Must enable speaker diarization first
    speech_understanding={
        "request": {
            "speaker_identification": {
                "speaker_type": "name",  # or "role"
                "known_values": ["Sarah Chen", "Michael Rodriguez", "Alex Kim"]
            }
        }
    }
)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("meeting_recording.mp3", config=config)

# Access results with identified speakers
for utterance in transcript.utterances:
    print(f"{utterance.speaker}: {utterance.text}")
