import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
"authorization": "<YOUR_API_KEY>"
}

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file

upload_url = "https://assembly.ai/wildfires.mp3"

data = {
"audio_url": upload_url,
"speech_models": ["universal-3-pro", "universal-2"],
"language_detection": True,
"speaker_labels": True
}

# Transcribe file

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

# Poll for transcription results

while True:
transcript = requests.get(polling_endpoint, headers=headers).json()

if transcript["status"] == "completed":
break

elif transcript["status"] == "error":
raise RuntimeError(f"Transcription failed: {transcript['error']}")

else:
time.sleep(3)

# Enable speaker identification

understanding_body = {
"transcript_id": transcript_id,
"speech_understanding": {
"request": {
"speaker_identification": {
"speaker_type": "name",
"known_values": ["Michel Martin", "Peter DeCarlo"] # Change these values to match the names of the speakers in your file
}
}
}
}

# Send the modified transcript to the Speech Understanding API

result = requests.post(
"https://llm-gateway.assemblyai.com/v1/understanding",
headers = headers,
json = understanding_body
).json()

# Access the results and print utterances to the terminal

for utterance in result["utterances"]:
print(f"{utterance['speaker']}: {utterance['text']}")