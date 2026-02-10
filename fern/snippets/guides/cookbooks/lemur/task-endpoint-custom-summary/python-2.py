import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Transcribe the audio
audio_url = "https://storage.googleapis.com/aai-web-samples/meeting.mp4"
data = {"audio_url": audio_url}

response = requests.post(base_url + "/v2/transcript", json=data, headers=headers)
transcript_id = response.json()['id']
polling_endpoint = base_url + "/v2/transcript/" + transcript_id

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()
    if transcription_result['status'] == 'completed':
        break
    elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
    else:
        time.sleep(3)
