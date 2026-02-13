import assemblyai as aai

aai.settings.api_key = "YOUR_API_KEY"

transcriber = aai.Transcriber()

# Configure transcription with translation
config = aai.TranscriptionConfig(
  speaker_labels=True,  # Enable speaker labels
  # language_detection=True,  # Enable language detection if you are processing files in a variety of languages
  speech_understanding=aai.SpeechUnderstandingConfig(
    translation=aai.TranslationConfig(
      target_languages=['es', 'de'],  # Translate to Spanish and German
      formal=True,  # Use formal language style
      match_original_utterance=True  # Get translated utterances
    )
  )
)

# Submit transcription request
transcript = transcriber.transcribe(
  "https://assembly.ai/wildfires.mp3",
  config=config
)

# Access and display results
print("\n--- Original Transcript ---")
print(transcript['text'][:200] + "...\n")

print("--- Translations ---")
for language_code, translated_text in transcript['translated_texts'].items():
  print(f"{language_code.upper()}:")
  print(translated_text[:200] + "...\n")
