transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()

    if transcription_result['status'] == 'completed':
        # Print each auto chapter
        for chapter in transcription_result['chapters']:
            print("Chapter Start Time:", chapter['start'])
            print("Chapter End Time:", chapter['end'])
            print("Chapter Gist:", chapter['gist'])
            print("Chapter Headline:", chapter['headline'])
            print("Chapter Summary:", chapter['summary'], '\n')
        break

    elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

    else:
        time.sleep(3)
