import requests

headers = {
  "authorization": "<YOUR_API_KEY>"
}

conversation_history = [
    {"role": "user", "content": "Where does Sarah work and what city is that in?"}
]

max_iterations = 10
iteration = 0

while iteration < max_iterations:
    iteration += 1
    response = chat(conversation_history, model)
    choice = response["choices"][0]

    if choice.get("tool_calls"):
        # Execute tools and add results to history
        handle_tool_calls(choice["tool_calls"], conversation_history)
        # Continue loop - model can make more tool calls
        continue
    else:
        # Model has final answer
        print(choice["message"]["content"])
        break
