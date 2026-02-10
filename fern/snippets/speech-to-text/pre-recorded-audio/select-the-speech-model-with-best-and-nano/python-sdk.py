import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"
# You can use a local filepath:
# audio_file = "./local_file.mp3"

# Or use a publicly-accessible URL:
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True
)
transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)
