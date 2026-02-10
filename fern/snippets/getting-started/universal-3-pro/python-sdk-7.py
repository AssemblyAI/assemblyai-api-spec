import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/speaker_diarization.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  speaker_labels=True,
  prompt="Produce a transcript with every disfluency data. Additionally, label speakers with their respective roles. 1. Place [Speaker:role] at the start of each speaker turn. Example format: [Speaker:NURSE] Hello there. How can I help you today? [Speaker:PATIENT] I'm feeling unwell. I have a headache.",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

for utterance in transcript.utterances:
  print(f"Speaker {utterance.speaker}: {utterance.text}")
