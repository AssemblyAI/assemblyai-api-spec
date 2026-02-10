# Use your AssemblyAI API Key for authorization.
headers = {"authorization": assembly_key, "content-type": "application/json"}

# Specify AssemblyAI's transcription API endpoint.
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

# Use the presigned URL as the `audio_url` in the POST request.
json = {"audio_url": p_url}

# Queue the audio file for transcription with a POST request.
post_response = requests.post(transcript_endpoint, json=json, headers=headers)
