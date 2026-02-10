def upload_file(file_path):
    """Upload a local audio file to AssemblyAI"""
    with open(file_path, "rb") as f:
        response = requests.post(f"{base_url}/v2/upload", headers=headers, data=f)
        if response.status_code != 200:
            print(f"Error uploading: {response.status_code}, {response.text}")
            response.raise_for_status()
        return response.json()["upload_url"]

def transcribe_audio(audio_url):
    """Submit audio for transcription with sentences enabled and poll until complete"""
    data = {
        "audio_url": audio_url,
        "auto_highlights": False,
        "sentiment_analysis": False,
        "entity_detection": False
    }

    response = requests.post(f"{base_url}/v2/transcript", headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error submitting transcription: {response.status_code}, {response.text}")
        response.raise_for_status()

    transcript_id = response.json()["id"]
    polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

    print("Transcribing...")
    while True:
        transcript = requests.get(polling_endpoint, headers=headers).json()
        if transcript["status"] == "completed":
            print("Transcription completed!")
            return transcript
        elif transcript["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcript['error']}")
        else:
            time.sleep(3)

def get_sentences(transcript_id):
    """Get sentences from a completed transcript"""
    sentences_endpoint = f"{base_url}/v2/transcript/{transcript_id}/sentences"
    response = requests.get(sentences_endpoint, headers=headers)

    if response.status_code != 200:
        print(f"Error getting sentences: {response.status_code}, {response.text}")
        response.raise_for_status()

    return response.json()["sentences"]
