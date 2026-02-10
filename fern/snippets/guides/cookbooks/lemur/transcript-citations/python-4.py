def process_with_llm_gateway(transcript_text, question, context=""):
    """Send transcript to LLM Gateway for question answering"""
    prompt = f"""Based on the following transcript, please answer this question:
            Question: {question}
            Context: {context}
            Transcript: {transcript_text}
            Please provide a clear and specific answer."""

    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 2000
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
