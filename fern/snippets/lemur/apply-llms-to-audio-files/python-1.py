import requests
import time

# Step 1: Transcribe the audio
base_url = "https://api.assemblyai.com"

headers = {
  "authorization": "<YOUR_API_KEY>"
}

# You can use a local filepath:
# with open("./my-audio.mp3", "rb") as f:
# response = requests.post(base_url + "/v2/upload",
# headers=headers,
# data=f)
# upload_url = response.json()["upload_url"]
# Or use a publicly-accessible URL:

upload_url = "https://assembly.ai/sports_injuries.mp3"

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

# Step 2: Send transcript to LLM Gateway
prompt = "Provide a brief summary of the transcript."

llm_gateway_data = {
  "model": "claude-sonnet-4-5-20250929",
  "messages": [
    {"role": "user", "content": f"{prompt}\n\nTranscript: {transcript['text']}"}
  ],
  "max_tokens": 1000
}

response = requests.post(
  "https://llm-gateway.assemblyai.com/v1/chat/completions",
  headers=headers,
  json=llm_gateway_data
)
print(response.json()["choices"][0]["message"]["content"])
