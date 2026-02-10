def process_with_llm_gateway(transcript_text, prompt):
    """Send transcript to LLM Gateway for processing"""
    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nTranscript:\n\n{transcript_text}"
            }
        ],
        "max_tokens": 1500
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()

    if "error" in result:
        raise RuntimeError(f"LLM Gateway error: {result['error']}")

    return result['choices'][0]['message']['content']
