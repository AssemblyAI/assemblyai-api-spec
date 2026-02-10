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
    "audio_url": upload_url # You can also use a URL to an audio or video file on the web
}

url = base_url + "/v2/transcript"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()['id']
polling_endpoint = url + "/" + transcript_id

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()

    if transcript['status'] == 'completed':
        print(f"Full Transcript:", transcript['text'])
        break

    elif transcript['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcript['error']}")

    else:
        time.sleep(3)
