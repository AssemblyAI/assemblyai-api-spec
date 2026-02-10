while max_tries > 0:
    max_tries -= 1
    job = transcribe_client.get_transcription_job(
        TranscriptionJobName=job_name
    )
    job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
    if job_status in ["COMPLETED", "FAILED"]:
        break
    time.sleep(10)
