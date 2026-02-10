curl -X POST \
  "https://llm-gateway.assemblyai.com/v1/chat/completions" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
      {
        "role": "user",
        "content": "Find employees in Engineering"
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "search_employees",
          "description": "Search employee database by name, department, or other criteria",
          "parameters": {
            "type": "object",
            "properties": {
              "department": {
                "type": "string",
                "description": "Department name"
              }
            }
          }
        }
      }
    ],
    "max_tokens": 1000
  }'
