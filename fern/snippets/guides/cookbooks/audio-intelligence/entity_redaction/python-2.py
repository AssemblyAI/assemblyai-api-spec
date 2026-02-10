transcriber = aai.Transcriber()

audio_url = (
    "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
)

config = aai.TranscriptionConfig(entity_detection=True)

transcript = transcriber.transcribe(audio_url, config)
