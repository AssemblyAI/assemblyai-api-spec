import requests
import time

# Step 1: Transcribe the audio
base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

audio_url = "https://assembly.ai/meeting.mp4"
data = {"audio_url": audio_url}
response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()
    if transcript["status"] == "completed":
        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    else:
        time.sleep(3)

# Step 2: Create structured Q&A prompt
questions = [
    "What are the top level KPIs for engineering? (KPI stands for key performance indicator)",
    "How many days has it been since the data team has gotten updated metrics? (Choose from: 1, 2, 3, 4, 5, 6, 7, more than 7)"
]

prompt = f"""Answer the following questions based on the meeting transcript. Format your response as:
Q1: [question]
A1: [answer]
Q2: [question]
A2: [answer]

Questions:
{". ".join([f"{i+1}. {q}" for i, q in enumerate(questions)])}

Context: This is a GitLab meeting to discuss logistics."""

# Step 3: Send to LLM Gateway
llm_gateway_data = {
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
        {"role": "user", "content": f"{prompt}\n\nTranscript: {transcript['text']}"}
    ],
    "max_tokens": 1000
}

result = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json=llm_gateway_data
)
print(result.json()["choices"][0]["message"]["content"])
