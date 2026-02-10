transcribe_client.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={"MediaFileUri": file_uri},
    Settings={
        "ShowSpeakerLabels": True,
        "MaxSpeakerLabels": 2
    }
)
