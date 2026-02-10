config = aai.TranscriptionConfig(
    language_detection=True,  # Auto-detect languages
    language_detection_options=aai.LanguageDetectionOptions(
        code_switching=True,  # Preserve language switches
        code_switching_confidence_threshold=0.5
    ),
    translation_language_code="en",  # Translate everything to English
)

transcript = transcriber.transcribe("multilingual_meeting.mp3", config=config)

# Original transcript preserves language switches
for utterance in transcript.utterances:
    detected_lang = utterance.language_code if hasattr(utterance, 'language_code') else "unknown"
    print(f"[{detected_lang}] {utterance.speaker}: {utterance.text}")

# Translation combines everything in English
print(f"\nEnglish translation:\n{transcript.translation}")
