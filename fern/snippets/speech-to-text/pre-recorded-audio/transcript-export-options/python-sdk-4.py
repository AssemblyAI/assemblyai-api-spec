import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True
)

transcript = aai.Transcriber().transcribe(audio_file, config)

for word in transcript.words:
  print(f"Word: {word.text}, Start: {word.start}, End: {word.end}, Confidence: {word.confidence}")
