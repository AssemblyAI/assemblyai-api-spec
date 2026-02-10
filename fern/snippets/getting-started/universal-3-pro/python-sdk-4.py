import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/ouput_formatting.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="Add punctuation based on the speaker's tone and expressiveness. Use exclamation marks (!) when the speaker is yelling, excited, or emphatic. Use question marks (?) for questioning intonation. Apply standard punctuation (periods, commas) based on natural speech patterns and pauses.",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
