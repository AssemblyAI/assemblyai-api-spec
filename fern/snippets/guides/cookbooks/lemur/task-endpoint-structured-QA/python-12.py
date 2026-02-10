# -------------------------------
# Step 5: Query LLM Gateway
# -------------------------------
headers = {"authorization": API_KEY}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json={
        "model": "claude-sonnet-4-5-20250929",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
    },
)

response_json = response.json()
llm_output = response_json["choices"][0]["message"]["content"]
