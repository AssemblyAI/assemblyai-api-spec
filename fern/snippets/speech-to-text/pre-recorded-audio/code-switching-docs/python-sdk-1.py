import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "./bilingual-audio.mp3"
# audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
    speech_models=["universal-2"],
    language_detection=True,
    language_detection_options=aai.LanguageDetectionOptions(
      code_switching=True
    )
)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)
