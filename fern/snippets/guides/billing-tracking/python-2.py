import requests

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Get transcript using the ID from webhook
response = requests.get(base_url + "/v2/transcript/<TRANSCRIPT_ID>", headers=headers)
transcript = response.json()

if transcript["status"] == "completed":
    audio_duration = transcript["audio_duration"]  # Duration in seconds
    # Use audio_duration for billing/tracking
