import assemblyai as aai
import requests

aai.settings.api_key = "<YOUR_API_KEY>"

# Step 1: Transcribe an audio file
audio_file = "https://assembly.ai/call.mp4"
transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_file)

# Step 2: Prepare for LLM Gateway
transcript_text = transcript.text
prompt = "What was the emotional sentiment of the phone call?"

headers = {"authorization": "<YOUR_API_KEY>"}

# Step 3: Send to LLM Gateway
response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json={
        "model": "claude-sonnet-4-20250514",
        "messages": [
            {
                "role": "user",
                "content": f"Analyze this phone call transcript for emotional sentiment:\n\n{transcript_text}\n\n{prompt}"
            }
        ],
        "max_tokens": 1000
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
