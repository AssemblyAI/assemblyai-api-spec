import assemblyai as aai

# Configure for medical encounter
config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.universal_3_pro,
    speaker_labels=True,
    speakers_expected=2,  # Doctor and patient

    # Enable speaker identification with medical roles
    speech_understanding={
        "request": {
            "speaker_identification": {
                "speaker_type": "role",
                "known_values": ["Doctor", "Patient"]
            }
        }
    }
)

# Transcribe medical encounter
transcript = await transcribe_async(audio_file, config)

# Results show clear role attribution
for utterance in transcript.utterances:
    print(f"{utterance.speaker}: {utterance.text}")
    # Output: "Doctor: What brings you in today?"
    #         "Patient: I've been having chest pain for the past week."
