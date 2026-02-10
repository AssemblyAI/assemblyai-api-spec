import requests

headers = {
    "authorization": "<YOUR_API_KEY>",
    "content-type": "application/json"
}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json={
        "model": "gemini-2.5-flash-lite",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful math tutor. Guide the user through the solution step by step."
            },
            {
                "role": "user",
                "content": "how can I solve 8x + 7 = -23"
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "math_reasoning",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": "string"},
                                    "output": {"type": "string"}
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False
                            }
                        },
                        "final_answer": {"type": "string"}
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
