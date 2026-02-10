config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.universal_3_pro,
    speaker_labels=True,
    speakers_expected=2,

    speech_understanding={
        "request": {
            "speaker_identification": {
                "speaker_type": "name",
                "known_values": ["Dr. Sarah Johnson", "Patient"]
            }
        }
    }
)
