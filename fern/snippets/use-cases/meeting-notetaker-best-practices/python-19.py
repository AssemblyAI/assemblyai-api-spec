config = aai.TranscriptionConfig(
    # Core transcription
    speaker_labels=True,

    # Speech Understanding
    summarization=True,
    sentiment_analysis=True,
    entity_detection=True,

    # PII protection
    redact_pii=True,
    redact_pii_policies=[
        PIIRedactionPolicy.person_name,
        PIIRedactionPolicy.email_address,
        PIIRedactionPolicy.phone_number,
    ],
    redact_pii_sub=PIISubstitutionPolicy.hash,
    redact_pii_audio=True,
)

transcript = transcriber.transcribe(audio_url, config=config)

# Access all features
meeting_insights = {
    "summary": transcript.summary,
    "sentiment_trend": analyze_sentiment_trend(transcript.sentiment_analysis_results),
    "entities": extract_entities(transcript.entities),
    "safe_transcript": transcript.text,  # PII redacted
    "safe_audio": transcript.redacted_audio_url,  # PII bleeped
}
