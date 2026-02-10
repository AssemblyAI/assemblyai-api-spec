import time
import boto3

def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="wav",
        LanguageCode="en-US",
    )

    max_tries = 60
    while max_tries > 0:
    max_tries -= 1

    job = transcribe_client.get_transcription_job(
        TranscriptionJobName=job_name
    )

    job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]

    if job_status in ["COMPLETED", "FAILED"]:
        print(f"Job {job_name} is {job_status}.")

    if job_status == "COMPLETED":
        print(
            f"Download the transcript from\n"
            f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}."
        )
        break
    else:
        print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)

def main():
    transcribe_client = boto3.client("transcribe")
    file_uri = "s3://test-transcribe/answer2.wav"
    transcribe_file("Example-job", file_uri, transcribe_client)

if name == "main":
    main()
