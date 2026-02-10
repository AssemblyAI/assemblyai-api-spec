result = response.json()

if "error" in result:
    print(f"\nError from LLM Gateway: {result['error']}")
else:
    response_text = result['choices'][0]['message']['content']
    print(f"\nResponse ID: {result["request_id"]}\n")
    print(response_text)
