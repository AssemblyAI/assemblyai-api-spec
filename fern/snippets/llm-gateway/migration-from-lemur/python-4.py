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
    transcript_data = status_response.json()
    if transcript_data["status"] == "completed":
        transcript_text = transcript_data["text"]
        break
    elif transcript_data["status"] == "error":
        raise RuntimeError("Transcription failed")
    time.sleep(3)

# Step 2: Send to LLM Gateway
prompt = "What was the emotional sentiment of the phone call?"
llm_data = {
    "model": "claude-sonnet-4-20250514",
    "messages": [
        {
            "role": "user",
            "content": f"Analyze this phone call transcript for emotional sentiment:\n\n{transcript_text}\n\n{prompt}"
        }
    ],
    "max_tokens": 1000
}

result = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json=llm_data
)
print(result.json()["choices"][0]["message"]["content"])
