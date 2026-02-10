import json

content = result["choices"][0]["message"]["content"]
parsed = json.loads(content)

for step in parsed["steps"]:
    print(f"{step['explanation']}: {step['output']}")

print(f"Final answer: {parsed['final_answer']}")
