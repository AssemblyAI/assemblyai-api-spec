import requests
import time

base_url = "https://api.assemblyai.com"

headers = {"authorization": "<YOUR_API_KEY>"}

# You can use a local filepath:
# with open("./my-audio.mp3", "rb") as f:
#     response = requests.post(base_url + "/v2/upload", headers=headers, data=f)
#     upload_url = response.json()["upload_url"]

# Or use a publicly-accessible URL:
upload_url = "https://assembly.ai/sports_injuries.mp3"

data = {"audio_url": upload_url}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()

    if transcript["status"] == "completed":
        break

    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")

    else:
        time.sleep(3)
