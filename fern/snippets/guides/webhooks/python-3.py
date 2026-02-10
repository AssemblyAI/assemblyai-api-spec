config = aai.TranscriptionConfig().set_webhook(
    "https://example.com/webhook", "X-My-Webhook-Secret", "secret-value"
)

aai.Transcriber().submit(audio_url, config)
