import requests

headers = {
  "authorization": "<YOUR_API_KEY>"
}

conversation_history = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What's the population?"}
]

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers = headers,
    json = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": conversation_history,
        "max_tokens": 1000
    }
)

result = response.json()
agent_response = result["choices"][0]["message"]["content"]
print(agent_response)

# Append the assistant's response to conversation history
conversation_history.append({"role": "assistant", "content": agent_response})
