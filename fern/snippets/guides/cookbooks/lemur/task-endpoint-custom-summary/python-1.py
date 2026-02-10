import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Step 1: Transcribe the audio
audio_url = "https://storage.googleapis.com/aai-web-samples/meeting.mp4"
data = {"audio_url": audio_url}

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

# Step 2: Generate custom summary with LLM Gateway
prompt = """
- You are an expert at writing factual, useful summaries.
- You focus on key details, leave out irrelevant information, and do not add in information that is not already present in the transcript.
- Your summaries accurately represent the information in the transcript.
- You are useful to the reader, are true and concise, and are written in perfect English.
- Use multiple parts of the transcript to form your summary.
- Make your summary follow the sequential order of events in the transcript.
- Your summaries do not describe the context of the transcript - they only summarize the events in the text.
- Your summaries do not describe what type of text they summarize.
- You do not dumb down specific language nor make big generalizations.
- Respond with just the summary and don't include a preamble or introduction.

Your summary should use the following format: Bullet points
"""

llm_gateway_data = {
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
        {"role": "user", "content": f"{prompt}\n\nTranscript: {transcription_result['text']}"}
    ],
    "max_tokens": 1500
}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json=llm_gateway_data
)

result = response.json()["choices"][0]["message"]["content"]
print(result)
