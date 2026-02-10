# Get transcript text first, then send to LLM Gateway
transcript_text = transcript.text

headers = {"authorization": "<YOUR_API_KEY>"}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json={
        "model": "claude-sonnet-4-20250514",
        "messages": [
            {
                "role": "user",
                "content": f"Analyze this transcript for emotional sentiment:\n\n{transcript_text}\n\nWhat was the emotional sentiment of the phone call?"
            }
        ],
        "max_tokens": 1000
    }
)

result = response.json()
answer = result["choices"][0]["message"]["content"]
