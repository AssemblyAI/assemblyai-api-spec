audio_url = "https://storage.googleapis.com/aai-web-samples/meeting.mp4"

# with open("/your_audio_file.mp3", "rb") as f:
#     response = requests.post(base_url + "/v2/upload", headers=headers, data=f)
#     if response.status_code != 200:
#         print(f"Error: {response.status_code}, Response: {response.text}")
#         response.raise_for_status()
#     upload_json = response.json()
#     audio_url = upload_json["upload_url"]

data = {
    "audio_url": audio_url,
}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

if response.status_code != 200:
    print(f"Error: {response.status_code}, Response: {response.text}")

transcript_json = response.json()
transcript_id = transcript_json["id"]
polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()
    if transcript["status"] == "completed":
        print(transcript['id'])
        print(f" \nFull Transcript: \n\n{transcript['text']}\n")

        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    else:
        time.sleep(3)
