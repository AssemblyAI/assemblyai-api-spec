import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
    "authorization": "<YOUR_API_KEY>"
}

with open("./local_file.mp3", "rb") as f:
    response = requests.post(base_url + "/v2/upload",
                            headers=headers,
                            data=f)

upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url, # You can also use a URL to an audio or video file on the web
    "speech_models": ["universal-3-pro", "universal-2"],
    "language_detection": True,
    "content_safety": True
}

url = base_url + "/v2/transcript"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()['id']
polling_endpoint = base_url + "/v2/transcript/" + transcript_id

print(f"Transcript ID:", transcript_id)

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()

    if transcription_result['status'] == 'completed':

        for result in transcription_result['content_safety_labels']['results']:
            print(result['text'])
            print(f"Timestamp: {result['timestamp']['start']} - {result['timestamp']['end']}")

            # Get category, confidence, and severity.
            for label in result['labels']:
                print(f"{label['label']} - {label['confidence']} - {label['severity']}")  # content safety category

        # Get the confidence of the most common labels in relation to the entire audio file.
        for label, confidence in transcription_result['content_safety_labels']['summary'].items():
            print(f"{confidence * 100}% confident that the audio contains {label}")

        # Get the overall severity of the most common labels in relation to the entire audio file.
        for label, severity_confidence in transcription_result['content_safety_labels']['severity_score_summary'].items():
            print(f"{severity_confidence['low'] * 100}% confident that the audio contains low-severity {label}")
            print(f"{severity_confidence['medium'] * 100}% confident that the audio contains medium-severity {label}")
            print(f"{severity_confidence['high'] * 100}% confident that the audio contains high-severity {label}")
        break
    elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
    else:
        time.sleep(3)
