import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True
)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

print(transcript.text)
print(transcript.json_response["language_confidence"])
