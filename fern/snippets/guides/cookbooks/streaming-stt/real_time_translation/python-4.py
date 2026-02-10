def translate_text(text):
    """Called when translating final transcripts."""
    headers = {
        "authorization": YOUR_API_KEY
    }

    llm_gateway_data = {
        "model": "claude-sonnet-4-20250514",
        "prompt": f"Translate the following text into Spanish. Do not write a preamble. Just return the translated text.\n\nText: {text}",
        "max_tokens": 1000
    }

    result = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )
    return result.json()["choices"][0]["message"]["content"]
