def extract_json(text):
    """Extract JSON from text that might contain markdown or extra text"""
    # First, try to remove markdown code blocks
    text = text.strip()

    # Remove ```json and ``` markers
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

    # Find the first { and last } to extract just the JSON object
    first_brace = text.find('{')
    last_brace = text.rfind('}')

    if first_brace != -1 and last_brace != -1:
        json_str = text[first_brace:last_brace + 1]
        return json.loads(json_str)

    # If that didn't work, try parsing the whole thing
    return json.loads(text)
