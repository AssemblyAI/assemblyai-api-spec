import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/entity_accuracy.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="The speaker is discussing the cancer drug Anktiva (spelled A-N-K-T-I-V-A). When you hear what sounds like Entiva or similar pronunciations, transcribe it as Anktiva. This is the correct pharmaceutical name.",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
