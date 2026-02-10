llm_gateway_data = {
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
        {"role": "user", "content": f"{prompt}\n\nTranscript: {transcription_result['text']}"}
    ],
    "max_tokens": 1500
}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json=llm_gateway_data
)

result = response.json()["choices"][0]["message"]["content"]
print(result)
