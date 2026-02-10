import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True,
    auto_chapters=True
)

transcript = aai.Transcriber().transcribe(audio_file, config)
print(f"Transcript ID:", transcript.id)

for chapter in transcript.chapters:
  print(f"{chapter.start}-{chapter.end}: {chapter.headline}")
