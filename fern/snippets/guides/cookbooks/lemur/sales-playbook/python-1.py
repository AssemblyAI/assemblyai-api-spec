import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Step 1: Transcribe the sales call
with open("./sales-call.mp3", "rb") as f:
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

# Step 2: Evaluate with LLM Gateway
context = "There are sales interactions between a salesperson who is selling an internet plan to customers who are warm leads."
answer_format = """
Answer with JSON in the following format:
{
    "Answer": "<answer_options>",
    "Reason": "<justification for the answer in one sentence including quotes>"
}
"""

questions = [
    {
        "question": "Did the salesperson start the conversation with a professional greeting?",
        "answer_options": ["Poor", "Satisfactory", "Excellent"]
    },
    {
        "question": "How well did the salesperson answer questions during the call?",
        "answer_options": ["Poor", "Good", "Excellent"]
    },
    {
        "question": "Did the salesperson discuss next steps clearly?",
        "answer_options": ["Yes", "No"]
    }
]

for q in questions:
    prompt = f"""
{q['question']}

Context: {context}

Answer Options: {', '.join(q['answer_options'])}

{answer_format}
"""

    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {"role": "user", "content": f"{prompt}\n\nTranscript: {transcription_result['text']}"}
        ],
        "max_tokens": 500
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()["choices"][0]["message"]["content"]
    print(f"Question: {q['question']}")
    print(f"Answer: {result}")
    print()
