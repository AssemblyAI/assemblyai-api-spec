import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "YOUR_API_KEY"}

# Use a publicly-accessible URL
audio_file = "https://assembly.ai/wildfires.mp3"

# Or upload a local file:
# with open("./example.mp3", "rb") as f:
#     response = requests.post(base_url + "/v2/upload", headers=headers, data=f)
#     if response.status_code != 200:
#         print(f"Error: {response.status_code}, Response: {response.text}")
#         response.raise_for_status()
#     upload_json = response.json()
#     audio_file = upload_json["upload_url"]

data = {
    "audio_url": audio_file,
    "speech_models": ["universal-3-pro", "universal-2"],
    "language_detection": True,
    "speaker_labels": True
}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

if response.status_code != 200:
    print(f"Error: {response.status_code}, Response: {response.text}")
    response.raise_for_status()

transcript_json = response.json()
transcript_id = transcript_json["id"]
polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()
    if transcript["status"] == "completed":
        print(f"\nFull Transcript:\n\n{transcript['text']}")

        # Optionally print speaker diarization results
        # for utterance in transcript['utterances']:
        #     print(f"Speaker {utterance['speaker']}: {utterance['text']}")
        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    else:
        time.sleep(3)
