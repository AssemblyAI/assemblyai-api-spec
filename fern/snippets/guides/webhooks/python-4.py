import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
    "authorization": "<YOUR_API_KEY>"
}

with open("./my-audio.mp3", "rb") as f:
  response = requests.post(base_url + "/v2/upload",
                          headers=headers,
                          data=f)

upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url,
    "webhook_url": "https://example.com/webhook",
    "webhook_auth_header_name": "X-My-Webhook-Secret",
    "webhook_auth_header_value": "secret-value"
}

url = base_url + "/v2/transcript"
response = requests.post(url, json=data, headers=headers)
