audio_file_path = "./meeting.mp3"
# ------------------------------------------
# Step 1: Upload the audio file
# ------------------------------------------
def upload_file(filename):
    with open(filename, "rb") as f:
        upload_url = "https://api.assemblyai.com/v2/upload"
        headers = {"authorization": API_KEY}
        response = requests.post(upload_url, headers=headers, data=f)
        response.raise_for_status()
        return response.json()["upload_url"]
audio_url = upload_file(audio_file_path)
print(f"Uploaded audio file. URL: {audio_url}")
# ------------------------------------------
# Step 2: Request transcription
# ------------------------------------------
transcript_request = requests.post(
    "https://api.assemblyai.com/v2/transcript",
    headers={"authorization": API_KEY, "content-type": "application/json"},
    json={"audio_url": audio_url},
)
transcript_id = transcript_request.json()["id"]
# Poll until completed
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
print("\nTranscription complete.\n")
