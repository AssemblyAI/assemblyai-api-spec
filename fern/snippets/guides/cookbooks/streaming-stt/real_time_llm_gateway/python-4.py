def analyze_with_llm_gateway(text):
    """Called when the WebSocket connection is closing and the transcript text is sent to LLM Gateway to be analyzed."""
    headers = {
        "authorization": YOUR_API_KEY,
        "content-type": "application/json"
    }

    prompt = "You are a helpful coach. Provide an analysis of the transcript and offer areas to improve with exact quotes. Include no preamble. Start with an overall summary then get into the examples with feedback."

    llm_gateway_data = {
        "model": "claude-sonnet-4-20250514",
        "messages": [
            {"role": "user", "content": f"{prompt}\n\nTranscript: {text}"}
        ],
        "max_tokens": 4000
    }

    result = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )
    return result.json()["choices"][0]["message"]["content"]
