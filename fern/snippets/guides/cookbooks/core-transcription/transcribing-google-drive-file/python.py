transcriber = aai.Transcriber()

audio_url = (
"https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3"
)

transcript = transcriber.transcribe(audio_url)
