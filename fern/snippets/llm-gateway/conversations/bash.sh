curl -X POST \
  "https://llm-gateway.assemblyai.com/v1/chat/completions" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
      {
        "role": "user",
        "content": "What is the capital of France?"
      },
      {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      {
        "role": "user",
        "content": "What'\''s the population?"
      }
    ],
    "max_tokens": 1000
  }'
