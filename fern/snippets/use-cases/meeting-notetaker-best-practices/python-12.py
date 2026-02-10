import assemblyai as aai

aai.settings.api_key = "your_api_key"

config = aai.TranscriptionConfig(
    language_code="es",  # Spanish audio
    translation_language_code="en",  # Translate to English
    speaker_labels=True,  # Maintain speaker labels
)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("spanish_meeting.mp3", config=config)

# Access original Spanish transcript
print("Original (Spanish):")
print(transcript.text)

# Access English translation
print("\nTranslation (English):")
print(transcript.translation)
