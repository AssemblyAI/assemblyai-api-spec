audio_url = "https://assembly.ai/wildfires.mp3"
data = {"audio_url": audio_url}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

# Poll for completion
print("Waiting for transcription to complete...")

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()
    if transcript["status"] == "completed":
        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    time.sleep(3)
