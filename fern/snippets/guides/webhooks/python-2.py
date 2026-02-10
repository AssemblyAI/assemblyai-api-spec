import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
    "authorization": "<YOUR_API_KEY>"
}

transcript_id = "<TRANSCRIPT_ID>"

polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

transcription_result = requests.get(polling_endpoint, headers=headers).json()

if transcription_result['status'] == 'completed':
  print(f"Transcript ID:", transcript_id)
elif transcription_result['status'] == 'error':
  raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
