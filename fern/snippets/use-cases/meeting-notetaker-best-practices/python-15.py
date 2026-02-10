async def process_international_meeting(audio_url: str, target_language: str = "en"):
    """
    Process multilingual meeting with translation and identification
    """
    config = aai.TranscriptionConfig(
        # Handle multiple languages
        language_detection=True,
        language_detection_options=aai.LanguageDetectionOptions(
            code_switching=True,
            code_switching_confidence_threshold=0.5
        ),

        # Translate to common language
        translation_language_code=target_language,

        # Speaker identification
        speaker_labels=True,

        # Generate summary in target language
        summarization=True,
    )

    transcriber = aai.Transcriber()
    transcript = await asyncio.to_thread(
        transcriber.transcribe,
        audio_url,
        config=config
    )

    return {
        "original_transcript": transcript.text,
        "translated_transcript": transcript.translation,
        "summary": transcript.summary,  # Already in target language
        "speakers": list(set(u.speaker for u in transcript.utterances)),
        "languages_detected": list(set(
            u.language_code for u in transcript.utterances
            if hasattr(u, 'language_code')
        ))
    }
