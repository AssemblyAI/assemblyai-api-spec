import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

data = {
    "audio_url": "https://assemblyaiassets.com/audios/speaker_diarization.mp3",
    "language_detection": True,
    "speech_models": ["universal-3-pro", "universal-2"],
    "speaker_labels": True,
    "prompt": "Produce a transcript with every disfluency data. Additionally, label speakers with their respective roles. 1. Place [Speaker:role] at the start of each speaker turn. Example format: [Speaker:NURSE] Hello there. How can I help you today? [Speaker:PATIENT] I'm feeling unwell. I have a headache."
}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

if response.status_code != 200:
    print(f"Error: {response.status_code}, Response: {response.text}")
    response.raise_for_status()

transcript_response = response.json()
transcript_id = transcript_response["id"]
polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()
    if transcript["status"] == "completed":
        for utterance in transcript["utterances"]:
            print(f"Speaker {utterance['speaker']}: {utterance['text']}")
        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    else:
        time.sleep(3)
