transcription_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()

    if transcription_result['status'] == 'completed':
        auto_highlights_result = transcription_result['auto_highlights_result']
        for highlight in auto_highlights_result['results']:
            print(f"Highlight: {highlight['text']}, Count: {highlight['count']}, Rank: {highlight['rank']}, Timestamps: {highlight['timestamps']}")
        break

    elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

    else:
        time.sleep(3)
