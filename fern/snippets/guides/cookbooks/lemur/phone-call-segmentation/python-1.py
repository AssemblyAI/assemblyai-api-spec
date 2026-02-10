import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
    "authorization": "<YOUR_API_KEY>"
}

# Step 1: Transcribe and get VTT subtitles
with open("./my-audio.mp3", "rb") as f:
    response = requests.post(base_url + "/v2/upload", headers=headers, data=f)

upload_url = response.json()["upload_url"]
data = {"audio_url": upload_url}

response = requests.post(base_url + "/v2/transcript", json=data, headers=headers)
transcript_id = response.json()['id']
polling_endpoint = base_url + "/v2/transcript/" + transcript_id

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()
    if transcription_result['status'] == 'completed':
        break
    elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
    else:
        time.sleep(3)

# Get VTT subtitles
vtt_response = requests.get(f"{polling_endpoint}/vtt", headers=headers)
vtt_content = vtt_response.text

# Step 2: Define phases and analyze with LLM Gateway
phases = ["Introduction", "Complaint", "Resolution", "Goodbye"]

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
