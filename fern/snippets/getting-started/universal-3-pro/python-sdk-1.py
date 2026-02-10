import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assembly.ai/sports_injuries.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
