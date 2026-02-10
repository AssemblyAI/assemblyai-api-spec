transcriber = aai.Transcriber()

# Local Files
transcript = transcriber.transcribe("./audio.mp3")

# Public URLs
transcript = transcriber.transcribe("https://example.com/audio.mp3")
