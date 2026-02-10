import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig().set_webhook("https://example.com/webhook", "X-My-Webhook-Secret", "secret-value")

aai.Transcriber().submit(audio_file, config)
