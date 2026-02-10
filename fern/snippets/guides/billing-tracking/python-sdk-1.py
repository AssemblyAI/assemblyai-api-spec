import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Add customer_id as a query parameter to your webhook URL
webhook_url = "https://your-domain.com/webhook?customer_id=customer_123"

config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.best
).set_webhook(webhook_url)

# Submit without waiting for completion
aai.Transcriber().submit("https://example.com/audio.mp3", config)
