import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/audio_tag.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="Produce a transcript suitable for conversational analysis. Every disfluency is meaningful data. Include: Tag sounds: [beep]",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
