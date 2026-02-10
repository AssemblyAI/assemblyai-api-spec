# HIPAA-compliant storage requirements
# - Encryption at rest (AES-256)
# - Encryption in transit (TLS 1.2+)
# - Access controls and audit logging
# - Automatic deletion after retention period

# Example with AWS S3
audio_url = "https://your-hipaa-compliant-s3.amazonaws.com/encounters/patient123.mp3"
# Ensure bucket has:
# - Server-side encryption enabled
# - Access logging enabled
# - Bucket policy restricting access
# - Lifecycle policy for automatic deletion
