import json
import os
import boto3
import http.client
import time
from urllib.parse import unquote_plus
import logging

# Configure logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration settings

# See config parameters here: https://www.assemblyai.com/docs/api-reference/transcripts/submit

ASSEMBLYAI_CONFIG = {
# 'language_code': 'en_us',
# 'multichannel': True,
# 'redact_pii': True,
}

# Initialize AWS services

s3_client = boto3.client('s3')

def get_presigned_url(bucket, key, expiration=3600):
    """Generate a presigned URL for the S3 object"""

    logger.info({
        "message": "Generating presigned URL",
        "bucket": bucket,
        "key": key,
        "expiration": expiration
    })

    s3_client_with_config = boto3.client(
        's3',
        config=boto3.session.Config(signature_version='s3v4')
    )

    return s3_client_with_config.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )

def delete_transcript_from_assemblyai(transcript_id, api_key):
    """
    Delete transcript data from AssemblyAI's database using their DELETE endpoint.

    Args:
    transcript_id (str): The AssemblyAI transcript ID to delete
    api_key (str): The AssemblyAI API key

    Returns:
    bool: True if deletion was successful, False otherwise
    """

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    conn = http.client.HTTPSConnection("api.assemblyai.com")

    try: # Send DELETE request to AssemblyAI API
        conn.request("DELETE", f"/v2/transcript/{transcript_id}", headers=headers)
        response = conn.getresponse()

        # Check if deletion was successful (HTTP 200)
        if response.status == 200:
            response_data = json.loads(response.read().decode())
            logger.info(f"Successfully deleted transcript {transcript_id} from AssemblyAI")
            return True
        else:
            error_message = response.read().decode()
            logger.error(f"Failed to delete transcript {transcript_id}: HTTP {response.status} - {error_message}")
            return False

    except Exception as e:
        logger.info(f"Error deleting transcript {transcript_id}: {str(e)}")
        return False
    finally:
        conn.close()

def transcribe_audio(audio_url, api_key):
    """Transcribe audio using AssemblyAI API with http.client"""
    logger.info({"message": "Starting audio transcription"})

    headers = {
    "authorization": api_key,
    "content-type": "application/json"
    }

    conn = http.client.HTTPSConnection("api.assemblyai.com")

    # Submit the audio file for transcription with config parameters

    request_data = {"audio_url": audio_url}

    # Add all configuration settings

    request_data.update(ASSEMBLYAI_CONFIG)

    json_data = json.dumps(request_data)
    conn.request("POST", "/v2/transcript", json_data, headers)
    response = conn.getresponse()

    if response.status != 200:
        raise Exception(f"Failed to submit audio for transcription: {response.read().decode()}")

    response_data = json.loads(response.read().decode())
    transcript_id = response_data['id']
    logger.info({"message": "Audio submitted for transcription", "transcript_id": transcript_id})

    # Poll for transcription completion

    while True:
        conn = http.client.HTTPSConnection("api.assemblyai.com")
        conn.request("GET", f"/v2/transcript/{transcript_id}", headers=headers)
        polling_response = conn.getresponse()
        polling_data = json.loads(polling_response.read().decode())

       if polling_data['status'] == 'completed':
           conn.close()
           logger.info({"message": "Transcription completed successfully"})
           return polling_data  # Return full JSON response instead of just text
       elif polling_data['status'] == 'error':
           conn.close()
           raise Exception(f"Transcription failed: {polling_data['error']}")

       conn.close()
       time.sleep(3)

def lambda_handler(event, context):
    """Lambda function to handle S3 events and process audio files"""
    try: # Get the AssemblyAI API key from environment variables
        api_key = os.environ.get('ASSEMBLYAI_API_KEY')
        if not api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")

       # Process each record in the S3 event
       for record in event.get('Records', []):
           # Get the S3 bucket and key
           bucket = record['s3']['bucket']['name']
           key = unquote_plus(record['s3']['object']['key'])

           # Generate a presigned URL for the audio file
           audio_url = get_presigned_url(bucket, key)

           # Get the full transcript JSON from AssemblyAI
           transcript_data = transcribe_audio(audio_url, api_key)

           # Prepare the transcript key - maintaining path structure but changing directory and extension
           transcript_key = key.replace('/CallRecordings/', '/AssemblyAITranscripts/', 1).replace('.wav', '.json')

           # Convert the JSON data to a string
           transcript_json_str = json.dumps(transcript_data, indent=2)

           # Upload the transcript JSON to the same bucket but in transcripts directory
           s3_client.put_object(
               Bucket=bucket,  # Use the same bucket
               Key=transcript_key,
               Body=transcript_json_str,
               ContentType='application/json'
           )
           logger.info({"message": "Transcript uploaded to transcript bucket successfully.", "key": transcript_key})

           # Uncomment the following line to delete transcript data from AssemblyAI after saving to S3
           # https://www.assemblyai.com/docs/api-reference/transcripts/delete
           # delete_transcript_from_assemblyai(transcript_data['id'], api_key)

       return {
           "statusCode": 200,
           "body": json.dumps({
               "message": "Audio file(s) processed successfully",
               "detail": "Transcripts have been stored in the AssemblyAITranscripts directory"
           })
       }

    except Exception as e:
       print(f"Error: {str(e)}")

       return {
            "statusCode": 500,
            "body": json.dumps({
            "message": "Error processing audio file(s)",
            "error": str(e)
            })
       }
