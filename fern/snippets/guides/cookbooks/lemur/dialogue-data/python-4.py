def upload_file(file_path):
    """Upload a local audio file to AssemblyAI"""
    with open(file_path, "rb") as f:
        response = requests.post(f"{base_url}/v2/upload", headers=headers, data=f)
        if response.status_code != 200:
            print(f"Error uploading {file_path}: {response.status_code}, {response.text}")
            response.raise_for_status()
        return response.json()["upload_url"]

def transcribe_audio(audio_url):
    """Submit audio for transcription and poll until complete"""
    # Submit transcription request
    data = {"audio_url": audio_url}
    response = requests.post(f"{base_url}/v2/transcript", headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error submitting transcription: {response.status_code}, {response.text}")
        response.raise_for_status()

    transcript_id = response.json()["id"]
    polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

    # Poll for completion
    while True:
        transcript = requests.get(polling_endpoint, headers=headers).json()
        if transcript["status"] == "completed":
            return transcript["text"]
        elif transcript["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcript['error']}")
        else:
            time.sleep(3)
