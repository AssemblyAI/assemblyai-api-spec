import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(speaker_labels=True)
transcript = aai.Transcriber().transcribe(audio_url, config)

# Enable speaker identification
understanding_config = aai.SpeechUnderstandingConfig(
  speaker_identification=aai.SpeakerIdentificationConfig(
    speaker_type="name",
    known_values=["Michel Martin", "Peter DeCarlo"]  # Change these values to match the names of the speakers in your file
  )
)

result = aai.SpeechUnderstanding().understand(
  transcript.id,
  understanding_config
)

# Access the results and print utterances to the terminal
for utterance in result.utterances:
  print(f"{utterance.speaker}: {utterance.text}")