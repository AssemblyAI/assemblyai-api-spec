import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# You can use a local filepath:
# audio_file = "./example.mp3"

# Or use a publicly-accessible URL:
audio_file = (
    "https://assembly.ai/wildfires.mp3"
)

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  speaker_labels=True,
)

transcript = aai.Transcriber().transcribe(audio_file, config)

for utterance in transcript.utterances:
  print(f"Speaker {utterance.speaker}: {utterance.text}")
