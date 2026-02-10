import requests

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Add customer_id as a query parameter to your webhook URL
webhook_url = "https://your-domain.com/webhook?customer_id=customer_123"

data = {
    "audio_url": "https://example.com/audio.mp3",
    "webhook_url": webhook_url
}

# Submit without waiting for completion
response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
transcript_id = response.json()["id"]
