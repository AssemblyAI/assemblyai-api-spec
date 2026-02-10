results = []

for paragraph in combined_paragraphs:
    prompt = "Summarize this text as a whole and provide start and end timestamps."

    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {"role": "user", "content": f"{prompt}\n\n{paragraph}"}
        ],
        "max_tokens": 1000
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()["choices"][0]["message"]["content"]
    results.append(result)

for result in results:
    print(f"{result}\n")
