import requests

headers = {
  "authorization": "<YOUR_API_KEY>"
}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers = headers,
    json = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "max_tokens": 1000
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
