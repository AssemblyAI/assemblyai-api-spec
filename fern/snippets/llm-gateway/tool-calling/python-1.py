import requests

headers = {
  "authorization": "<YOUR_API_KEY>"
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_employees",
            "description": "Search employee database by name, department, or other criteria",
            "parameters": {
                "type": "object",
                "properties": {
                    "first_name": {
                        "type": "string",
                        "description": "Employee's first name"
                    },
                    "department": {
                        "type": "string",
                        "description": "Department name"
                    }
                },
                "required": []
            }
        }
    }
]

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers = headers,
    json={
        "model": "claude-sonnet-4-5-20250929",
        "messages": [{"role": "user", "content": "Find employees in Engineering"}],
        "tools": tools
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
