transcript_id = response.json()['id']
polling_endpoint = url + "/" + transcript_id

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()

    if transcript['status'] == 'completed':
        print(f"Full Transcript:", transcript['text'])
        break

    elif transcript['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcript['error']}")

    else:
        time.sleep(3)
