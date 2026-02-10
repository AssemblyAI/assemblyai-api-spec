import json

try:
    content = result["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    # Validate required fields exist
    if "steps" not in parsed or "final_answer" not in parsed:
        raise ValueError("Missing required fields in response")

except json.JSONDecodeError as e:
    print(f"Failed to parse response as JSON: {e}")
except KeyError as e:
    print(f"Unexpected response structure: {e}")
