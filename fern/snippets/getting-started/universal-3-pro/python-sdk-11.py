import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/Difficult_audio.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="When multiple speakers talk simultaneously, mark crosstalk segments.",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
