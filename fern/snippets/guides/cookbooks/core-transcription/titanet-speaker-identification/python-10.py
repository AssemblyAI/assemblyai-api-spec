transcript_obj = transcribe("https://api.assemblyai-solutions.com/storage/v1/object/sign/sam_training_bucket/elon_altman_interview_clipped.wav?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzYW1fdHJhaW5pbmdfYnVja2V0L2Vsb25fYWx0bWFuX2ludGVydmlld19jbGlwcGVkLndhdiIsImlhdCI6MTcwMDY5MDU3OSwiZXhwIjoxNzMyMjI2NTc5fQ.4qZHvVRGhNGttfcpcfXDcJkJe_tbkc_2Bvs4i51SNSE&t=2023-11-22T22%3A02%3A59.429Z")
wav_file = download_and_convert_to_wav("https://api.assemblyai-solutions.com/storage/v1/object/sign/sam_training_bucket/elon_altman_interview_clipped.wav?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzYW1fdHJhaW5pbmdfYnVja2V0L2Vsb25fYWx0bWFuX2ludGVydmlld19jbGlwcGVkLndhdiIsImlhdCI6MTcwMDY5MDU3OSwiZXhwIjoxNzMyMjI2NTc5fQ.4qZHvVRGhNGttfcpcfXDcJkJe_tbkc_2Bvs4i51SNSE&t=2023-11-22T22%3A02%3A59.429Z")
identified_utterances, unknown_speakers = identify_speakers_from_utterances(transcript_obj, wav_file)

for utterance in identified_utterances:
    print(f"{utterance['speaker']}: {utterance['text']}")
