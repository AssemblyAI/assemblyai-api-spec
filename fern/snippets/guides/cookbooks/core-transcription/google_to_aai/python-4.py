transcriber = aai.Transcriber()

# Local files
transcript = transcriber.transcribe("./audio.mp3")

# Public URLs
transcript = transcriber.transcribe("https://example.com/audio.mp3")

# S3 files (using pre-signed URLs)
s3_client = boto3.client('s3')
presigned_url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'audio.mp3'},
    ExpiresIn=3600
)
transcript = transcriber.transcribe(presigned_url)
