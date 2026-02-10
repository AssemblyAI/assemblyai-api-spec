import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/numbers_formatting.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="Transcribe with numbers normalized to standard formats. For example, when you see $1 billion, convert to $1,000,000,000.",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
