import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True,
    entity_detection=True
)

transcript = aai.Transcriber().transcribe(audio_file, config)
print(f"Transcript ID:", transcript.id)

for entity in transcript.entities:
    print(entity.text)
    print(entity.entity_type)
    print(f"Timestamp: {entity.start} - {entity.end}\n")
