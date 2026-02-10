import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/code_switching_multilingual.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="The spoken language may change throughout the audio, transcribe in the original language mix (code-switching), preserving the words in the language they are spoken.",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
