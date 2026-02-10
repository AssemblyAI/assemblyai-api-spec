transcriber = aai.Transcriber()

audio_url = (
    "https://www.listennotes.com/e/p/accd617c94a24787b2e0800f264b7a5e/"
)

config = aai.TranscriptionConfig(speaker_labels=True)
transcript = transcriber.transcribe(audio_url, config)
