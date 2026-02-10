import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True,
).set_redact_pii(
    policies=[
        aai.PIIRedactionPolicy.person_name,
        aai.PIIRedactionPolicy.organization,
        aai.PIIRedactionPolicy.occupation,
    ],
    substitution=aai.PIISubstitutionPolicy.hash,
)

transcript = aai.Transcriber().transcribe(audio_file, config)
print(f"Transcript ID:", transcript.id)

print(transcript.text)
