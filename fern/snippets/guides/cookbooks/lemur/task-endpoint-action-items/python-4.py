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
