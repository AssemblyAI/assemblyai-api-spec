import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Step 1: Transcribe audio
audio_data = {"audio_url": "https://assembly.ai/call.mp4"}
transcript_response = requests.post(f"{base_url}/v2/transcript", headers=headers, json=audio_data)
transcript_id = transcript_response.json()["id"]

# Poll for completion
while True:
    status_response = requests.get(f"{base_url}/v2/transcript/{transcript_id}", headers=headers)
    status = status_response.json()["status"]
    if status == "completed":
        break
    elif status == "error":
        raise RuntimeError("Transcription failed")
    time.sleep(3)

# Step 2: Apply LeMUR
lemur_data = {
    "prompt": "What was the emotional sentiment of the phone call?",
    "transcript_ids": [transcript_id],
    "final_model": "anthropic/claude-sonnet-4-20250514"
}

result = requests.post(f"{base_url}/lemur/v3/generate/task", headers=headers, json=lemur_data)
print(result.json()["response"])
