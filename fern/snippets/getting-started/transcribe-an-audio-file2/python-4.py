polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()

    if transcript["status"] == "completed":
        print(f"\nFull Transcript:\n\n{transcript['text']}")
        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    else:
        time.sleep(3)
