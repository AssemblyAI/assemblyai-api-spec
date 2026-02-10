import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/nlp_prompting.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="Produce a transcript for a clinical history evaluation. It's important to capture medication and dosage accurately. Every disfluency is meaningful data. Include: fillers (um, uh, er, erm, ah, hmm, mhm, like, you know, I mean), repetitions (I I I, the the), restarts (I was- I went), stutters (th-that, b-but, no-not), and informal speech (gonna, wanna, gotta)",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
