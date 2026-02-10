import assemblyai as aai

# Set your API key
aai.settings.api_key = "<YOUR_API_KEY>"

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
  speaker_labels=True,
  # language_detection=True,  # Enable language detection if you are processing files in a variety of languages
)
transcript = aai.Transcriber().transcribe(audio_file, config)

# Transcribe the audio
transcript = transcriber.transcribe(audio_url)

if transcript.status == aai.TranscriptStatus.error:
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print("Transcription completed!")

# Request translation using Speech Understanding
result = transcript.speech_understanding(
  translation={
    "target_languages": ["es", "de"],  # Translate to Spanish and German
    "formal": True,  # Use formal language style
    "match_original_utterance": True  # Get translated utterances (if speaker_labels was enabled)
  }
)

# Access and display results
print("\n--- Original Transcript ---")
print(transcript['text'][:200] + "...\n")

print("--- Translations ---")
for language_code, translated_text in transcript['translated_texts'].items():
  print(f"{language_code.upper()}:")
  print(translated_text[:200] + "...\n")
