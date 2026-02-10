for q in questions:
    prompt = f"""
{q['question']}

Context: {context}

Answer Options: {', '.join(q['answer_options'])}

{answer_format}
"""

    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {"role": "user", "content": f"{prompt}\n\nTranscript: {transcription_result['text']}"}
        ],
        "max_tokens": 500
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()["choices"][0]["message"]["content"]
    print(f"Question: {q['question']}")
    print(f"Answer: {result}")
    print()
