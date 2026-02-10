config = aai.TranscriptionConfig().set_redact_pii(
    policies=[
        aai.PIIRedactionPolicy.person_name,
        aai.PIIRedactionPolicy.organization,
        aai.PIIRedactionPolicy.occupation,
    ],
    redact_audio=True
)

transcript = aai.Transcriber().transcribe(audio_url, config)

print(transcript.get_redacted_audio_url())
