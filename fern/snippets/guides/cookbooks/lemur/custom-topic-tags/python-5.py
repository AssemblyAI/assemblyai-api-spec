prompt = f"""
You are a helpful assistant designed to label video content with topic tags.

I will give you a list of topics and definitions. Select the most relevant topic from the list. Return your selection and nothing else.

<topics_list>
{tag_list}
</topics_list>
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
print(result.strip())
