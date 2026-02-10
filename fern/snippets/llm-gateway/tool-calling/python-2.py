import requests
import json

headers = {
  "authorization": "<YOUR_API_KEY>"
}

choice = response.json()["choices"][0]

if choice.get("tool_calls"):
    tool_call = choice["tool_calls"][0]

    # Add function call to history
    conversation_history.append({
        "type": "function_call",
        "tool_call_id": tool_call["id"],
        "name": tool_call["function"]["name"],
        "arguments": tool_call["function"]["arguments"]
    })

    # Execute your function
    result = execute_function(
        tool_call["function"]["name"],
        json.loads(tool_call["function"]["arguments"])
    )

    # Add function output to history
    conversation_history.append({
        "type": "function_call_output",
        "tool_call_id": tool_call["id"],
        "name": tool_call["function"]["name"],
        "output": json.dumps({"result": result})
    })

    # Continue conversation with the result
    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers = headers,
        json = {
            "model": "claude-sonnet-4-5-20250929",
            "messages": conversation_history,
            "tools": tools
        }
    )

result = response.json()
print(result["choices"][0]["message"]["content"])
