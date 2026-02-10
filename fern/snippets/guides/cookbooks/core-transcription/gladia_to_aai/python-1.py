import requests
import time

base_url = "https://api.gladia.io"

headers = {
    "x-gladia-key": "<YOUR_API_KEY>"
}

with open("./my-audio.mp3", "rb") as f:
    files = {"audio": ("my-audio.mp3", f, "audio/mp3")}
    response = requests.post(base_url + "/v2/upload",
                            headers=headers,
                            files=files)

upload_url = response.json()["audio_url"]

data = {
    "audio_url": upload_url # You can also use a URL to an audio or video file on the web.
}

url = base_url + "/v2/pre-recorded"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()['id'] # You can also use response.json()['result_url'] to get the polling_endpoint directly.
polling_endpoint = url + "/" + transcript_id

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()

    if transcript['status'] == 'done':
        print(f"Full Transcript:", transcript['result']['transcription']['full_transcript'])
        break

    elif transcript['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcript['error_code']}")

    else:
        time.sleep(3)
