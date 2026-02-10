prompt = f'''
Analyze the following transcript of a phone call conversation and divide it into the following phases:
{', '.join(phases)}

You will be given the transcript in the format of VTT captions.

For each phase:
1. Identify the start and end timestamps (in seconds)
2. Provide a brief summary of what happened in that phase

Format your response as a JSON object with the following structure:
{{
    "phases": [
        {{
            "name": "Phase Name",
            "start_time": start_time_in_seconds,
            "end_time": end_time_in_seconds,
            "summary": "Brief summary of the phase"
        }},
        ...
    ]
}}

Ensure that all parts of the conversation are covered by a phase, using "Other" for any parts that don't fit into the specified phases.
'''

llm_gateway_data = {
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
        {"role": "user", "content": f"{prompt}\n\nVTT Transcript:\n{vtt_content}"}
    ],
    "max_tokens": 2000
}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json=llm_gateway_data
)

result = response.json()["choices"][0]["message"]["content"]
print(result)
