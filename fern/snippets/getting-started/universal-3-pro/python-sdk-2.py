import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/keyterms_prompting.wav"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  keyterms_prompt=["Kelly Byrne-Donoghue"],
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
