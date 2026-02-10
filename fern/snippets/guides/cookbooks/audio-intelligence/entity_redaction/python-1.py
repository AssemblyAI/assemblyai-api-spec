import assemblyai as aai
aai.settings.api_key = "YOUR_API_KEY"

transcriber = aai.Transcriber()

audio_url = (
    "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
)

config = aai.TranscriptionConfig(entity_detection=True)

transcript = transcriber.transcribe(audio_url, config)
redacted_transcript = transcript.text

# redact ALL entities
for entity in transcript.entities:
    redacted_transcript = redacted_transcript.replace(entity.text, f"[{entity.entity_type.upper()}]")

print(redacted_transcript[:500])
