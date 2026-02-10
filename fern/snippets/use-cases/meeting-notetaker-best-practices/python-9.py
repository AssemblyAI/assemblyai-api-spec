config = aai.TranscriptionConfig(
    speaker_labels=True,
    speech_understanding={
        "request": {
            "speaker_identification": {
                "speaker_type": "role",
                "known_values": ["Agent", "Customer"]  # or ["Interviewer", "Interviewee"]
            }
        }
    }
)
