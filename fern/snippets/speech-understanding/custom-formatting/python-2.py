import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/phone-msg.m4a"

# Configure transcription with custom formatting
config = aai.TranscriptionConfig(
  speaker_labels=True,
  speech_understanding=aai.SpeechUnderstandingConfig(
    request=aai.SpeechUnderstandingRequest(
      custom_formatting=aai.CustomFormatting(
        date="mm/dd/yyyy",
        phone_number="(xxx)xxx-xxxx",
        email="username@domain.com",
        format_utterances=True
      )
    )
  )
)

# Submit transcription and wait for results
transcriber = aai.Transcriber(config=config)
transcript = transcriber.transcribe(audio_url)

# Access and display results
print("\n--- Formatting Details ---")
mapping = transcript.speech_understanding.response.custom_formatting.mapping
for original, formatted in mapping.items():
  print(f"Original: {original}")
  print(f"Formatted: {formatted}\n")
