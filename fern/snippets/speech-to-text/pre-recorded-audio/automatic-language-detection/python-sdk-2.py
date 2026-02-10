import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

options = aai.LanguageDetectionOptions(
    expected_languages=["en", "es", "fr", "de"],
    fallback_language="auto"
)

config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True,
    language_detection_options=options
)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

print(transcript.text)
print(transcript.json_response["language_code"])
