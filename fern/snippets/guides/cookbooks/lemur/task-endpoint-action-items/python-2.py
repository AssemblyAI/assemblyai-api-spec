# Step 1: Upload or provide audio URL and start transcription
audio_url = "https://storage.googleapis.com/aai-web-samples/meeting.mp4"

transcript_request = requests.post(
    "https://api.assemblyai.com/v2/transcript",
    headers={"authorization": API_KEY, "content-type": "application/json"},
    json={"audio_url": audio_url},
)

transcript_id = transcript_request.json()["id"]

# Step 2: Poll until transcription completes
while True:
    polling_response = requests.get(
        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
        headers={"authorization": API_KEY},
    )
    status = polling_response.json()["status"]

    if status == "completed":
        transcript_text = polling_response.json()["text"]
        break
    elif status == "error":
        raise RuntimeError(f"Transcription failed: {polling_response.json()['error']}")
    else:
        print(f"Transcription status: {status}")
        time.sleep(3)
