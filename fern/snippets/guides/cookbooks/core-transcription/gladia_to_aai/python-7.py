transcript_id = response.json()['id'] # You can also use response.json()['result_url'] to get the polling_endpoint directly.
polling_endpoint = url + "/" + transcript_id

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()

    if transcript['status'] == 'done':
        print(f"Full Transcript:", transcript['result']['transcription']['full_transcript'])
        break

    elif transcript['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcript['error_code']}")

    else:
        time.sleep(3)
