import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
  "authorization": "<YOUR_API_KEY>"
}

upload_url = "https://assembly.ai/meeting.mp4"

data = {
  "audio_url": upload_url
}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

while True:
  transcript = requests.get(polling_endpoint, headers=headers).json()

  if transcript["status"] == "completed":
    break

  elif transcript["status"] == "error":
    raise RuntimeError(f"Transcription failed: {transcript['error']}")

  else:
    time.sleep(3)

lemur_data = {
  "transcript_ids": [transcript_id],
  "final_model": "anthropic/claude-sonnet-4-20250514",
  "context": "A GitLab meeting to discuss logistics",
  "answer_format": "TLDR"
}

result = requests.post(base_url + "/lemur/v3/generate/summary", headers=headers, json=lemur_data)

print(result.json()["response"])
