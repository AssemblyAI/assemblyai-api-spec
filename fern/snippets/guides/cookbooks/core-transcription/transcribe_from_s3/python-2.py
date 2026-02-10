# Create a low-level service client with the IAM credentials.
s3_client = boto3.client(
    "s3", aws_access_key_id=iam_access_id, aws_secret_access_key=iam_secret_key
)

# Generate a pre-signed URL for the audio file that expires after 30 minutes.
try:
    p_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=1800,
    )

except ClientError as e:
    logging.error(e)
