# For Method 1 (transcribe and identify in one request):
data = {
  "audio_url": upload_url,
  "speaker_labels": True,
  "speech_understanding": {
    "request": {
      "speaker_identification": {
        "speaker_type": "role",
        "known_values": ["Interviewer", "Interviewee"]  # Roles instead of names
      }
    }
  }
}

# For Method 2 (add identification to existing transcript):
understanding_body = {
  "transcript_id": transcript_id,
  "speech_understanding": {
    "request": {
      "speaker_identification": {
        "speaker_type": "role",
        "known_values": ["Interviewer", "Interviewee"]  # Roles instead of names
      }
    }
  }
}

# Send the modified transcript to the Speech Understanding API
result = requests.post(
  "https://llm-gateway.assemblyai.com/v1/understanding",
  headers = headers,
  json = understanding_body
).json()