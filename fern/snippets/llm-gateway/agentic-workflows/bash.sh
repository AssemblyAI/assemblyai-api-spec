curl -X POST \
  "https://llm-gateway.assemblyai.com/v1/chat/completions" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
      {
        "role": "user",
        "content": "Where does Sarah work and what city is that in?"
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "search_employees",
          "description": "Search employee database",
          "parameters": {
            "type": "object",
            "properties": {
              "first_name": {
                "type": "string"
              }
            }
          }
        }
      },
      {
        "type": "function",
        "function": {
          "name": "search_web",
          "description": "Search the web for information",
          "parameters": {
            "type": "object",
            "properties": {
              "query": {
                "type": "string"
              }
            }
          }
        }
      }
    ],
    "max_tokens": 1000
  }'
