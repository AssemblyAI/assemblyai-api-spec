import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

data = {
    "audio_url": "https://assemblyaiassets.com/audios/ouput_formatting.mp3",
    "language_detection": True,
    "speech_models": ["universal-3-pro", "universal-2"],
    "prompt": "Add punctuation based on the speaker's tone and expressiveness. Use exclamation marks (!) when the speaker is yelling, excited, or emphatic. Use question marks (?) for questioning intonation. Apply standard punctuation (periods, commas) based on natural speech patterns and pauses."
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
        print(transcript["text"])
        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    else:
        time.sleep(3)
