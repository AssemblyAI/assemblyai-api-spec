import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_file = "https://assemblyaiassets.com/audios/verbatim.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True,
  prompt="Produce a transcript suitable for conversational analysis. Every disfluency is meaningful data. Include: fillers (um, uh, er, ah, hmm, mhm, like, you know, I mean), repetitions (I I, the the), restarts (I was- I went), stutters (th-that, b-but, no-not), and informal speech (gonna, wanna, gotta)",
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.text)
