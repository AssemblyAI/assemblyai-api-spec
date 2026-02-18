import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/phone-msg.m4a"

config = aai.TranscriptionConfig(
  speaker_labels=True,
)

# Submit transcription request (without formatting)
transcript = aai.Transcriber().transcribe(audio_file, config)

print(f"Transcription completed! ID: {transcript.id}")

# Add custom formatting configuration to the completed transcript
understanding_config = aai.UnderstandingConfig(
  custom_formatting=aai.CustomFormattingConfig(
    date="mm/dd/yyyy",
    phone_number="(xxx)xxx-xxxx",
    email="username@domain.com",
    format_utterances=True
  )
)

# Send to Speech Understanding API for formatting
result = transcript.understanding(understanding_config)

# Access and display results
print("\n--- Formatting Details ---")
for original, formatted in result.custom_formatting.mapping.items():
  print(f"Original: {original}")
  print(f"Formatted: {formatted}\n")
