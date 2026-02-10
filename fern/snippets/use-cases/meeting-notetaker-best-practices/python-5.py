config = aai.TranscriptionConfig(
    webhook_url="https://your-app.com/webhooks/assemblyai",
    webhook_auth_header_name="X-Webhook-Secret",
    webhook_auth_header_value="your_secret_here",
    speaker_labels=True,
    summarization=True,
    # ... other config
)

# Submit job and return immediately (non-blocking)
transcript = transcriber.submit(audio_url, config=config)
print(f"Job submitted: {transcript.id}")
# Your app can continue processing other requests

# Your webhook receives results when ready (typically 15-30% of audio duration)
