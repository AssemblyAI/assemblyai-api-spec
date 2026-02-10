transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    # when the transcript is complete, extract all utterances from the response
    transcript_text = transcription_result['text']
    utterances = transcription_result['utterances']

    # For each utterance, print its speaker and what was said
    for utterance in utterances:
        speaker = utterance['speaker']
        text = utterance['text']
        print(f"Speaker {speaker}: {text}")

    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)
