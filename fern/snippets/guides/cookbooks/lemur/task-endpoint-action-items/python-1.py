import requests
import time

API_KEY = "YOUR_API_KEY"
audio_url = "https://storage.googleapis.com/aai-web-samples/meeting.mp4"

# Step 1: Upload or provide audio URL and start transcription
transcript_request = requests.post(
    "https://api.assemblyai.com/v2/transcript",
    headers={"authorization": API_KEY, "content-type": "application/json"},
    json={"audio_url": audio_url},
)

transcript_id = transcript_request.json()["id"]

# Step 2: Poll until transcription completes
while True:
    polling_response = requests.get(
        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
        headers={"authorization": API_KEY},
    )
    status = polling_response.json()["status"]

    if status == "completed":
        transcript_text = polling_response.json()["text"]
        break
    elif status == "error":
        raise RuntimeError(f"Transcription failed: {polling_response.json()['error']}")
    else:
        print(f"Transcription status: {status}")
        time.sleep(3)

# Step 3: Build the prompt
prompt = """
Here are guidelines to follow:
- You are an expert at understanding transcripts of conversations, calls and meetings.
- You are an expert at coming up with ideal action items based on the contents of the transcripts.
- Action items are things that the transcript implies should get done.
- Your action item ideas do not make stuff up that isn't relevant to the transcript.
- You do not needlessly make up action items - you stick to important tasks.
- You are useful, true and concise, and write in perfect English.
- Your action items can be tied back to direct quotes in the transcript.
- You do not cite the quotes the action items relate to.
- The action items are written succinctly.
- Please give useful action items based on the transcript.
"""

answer_format = "Bullet Points"
if answer_format:
    prompt += f"\nYour response should have the following format: {answer_format}"

# Step 4: Send transcript text to LLM Gateway
headers = {"authorization": API_KEY}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json={
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nTranscript:\n{transcript_text}",
            }
        ],
        "max_tokens": 1000,
    },
)

# Step 5: Print the LLM-generated action items
response_json = response.json()
print(response_json["choices"][0]["message"]["content"])
