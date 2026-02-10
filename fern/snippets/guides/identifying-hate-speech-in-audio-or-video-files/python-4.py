transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
   transcription_result = requests.get(polling_endpoint, headers=headers).json()

   if transcription_result['status'] == 'completed':
       # Uncomment the next line to print everything
       # print(transcription_result['content_safety_labels'])

       content_safety_labels = transcription_result['content_safety_labels']['results']
       for results in content_safety_labels:
           labels = results['labels']
           for label in labels:
             # The severity score measures how severe the flagged content is on a scale of 0-1, with 1 being the most severe.
             if label['label'] == 'hate_speech' and label['severity'] >= 0.5:
                 print("Hate speech detected with severity score:", label['severity'])
                 # Do something with this information, such as flagging the transcription for review
       break

   elif transcription_result['status'] == 'error':
       raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

   else:
       time.sleep(3)
