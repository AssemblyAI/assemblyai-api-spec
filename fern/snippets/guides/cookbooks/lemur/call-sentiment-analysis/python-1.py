import requests
import time
import json

API_KEY = "YOUR_API_KEY"
audio_file_path = "./meeting.mp3"

# ------------------------------------------
# Step 1: Upload the audio file
# ------------------------------------------
def upload_file(filename):
    with open(filename, "rb") as f:
        upload_url = "https://api.assemblyai.com/v2/upload"
        headers = {"authorization": API_KEY}
        response = requests.post(upload_url, headers=headers, data=f)
        response.raise_for_status()
        return response.json()["upload_url"]

audio_url = upload_file(audio_file_path)
print(f"Uploaded audio file. URL: {audio_url}")

# ------------------------------------------
# Step 2: Request transcription
# ------------------------------------------
transcript_request = requests.post(
    "https://api.assemblyai.com/v2/transcript",
    headers={"authorization": API_KEY, "content-type": "application/json"},
    json={"audio_url": audio_url},
)

transcript_id = transcript_request.json()["id"]

# Poll until completed
while True:
    polling_response = requests.get(
        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
        headers={"authorization": API_KEY},
    )
    status = polling_response.json()["status"]

    if status == "completed":
        transcript_text = polling_response.json()["text"]
        break
    elif status == "error":
        raise RuntimeError(f"Transcription failed: {polling_response.json()['error']}")
    else:
        print(f"Transcription status: {status}")
        time.sleep(3)

print("\nTranscription complete.\n")

# ------------------------------------------
# Step 3: Define questions
# ------------------------------------------
agent_context = "The agent is trying to get the customer to go through with the update to their car."
customer_context = "The customer is calling to check how much it would cost to update the map in his car."

answer_format = "<answer in one sentence> <reason in one sentence>"

questions = [
    {
        "question": "What was the overall sentiment of the call?",
        "context": customer_context,
        "answer_format": answer_format,
    },
    {
        "question": "What was the sentiment of the agent in this call?",
        "context": agent_context,
        "answer_format": answer_format,
    },
    {
        "question": "What was the sentiment of the customer in this call?",
        "context": customer_context,
        "answer_format": answer_format,
    },
    {
        "question": "What quote best demonstrates the customer's level of interest?",
        "context": customer_context,
        "answer_format": answer_format,
    },
    {
        "question": "Provide a quote from the agent that demonstrates their level of enthusiasm.",
        "context": agent_context,
        "answer_format": answer_format,
    },
]

# ------------------------------------------
# Step 4: Build prompt for the LLM
# ------------------------------------------
question_strs = []
for q in questions:
    q_str = f"Question: {q['question']}"
    if q.get("context"):
        q_str += f"\nContext: {q['context']}"
    if q.get("answer_format"):
        q_str += f"\nAnswer Format: {q['answer_format']}"
    question_strs.append(q_str)

questions_prompt = "\n\n".join(question_strs)

prompt = f"""
You are an expert at analyzing call transcripts.
Given the series of questions below, answer them accurately and concisely.
When context or answer format is provided, use it to guide your answers.

Transcript:
{transcript_text}

Questions:
{questions_prompt}
"""

# ------------------------------------------
# Step 5: Query the LLM Gateway
# ------------------------------------------
headers = {"authorization": API_KEY}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json={
        "model": "claude-sonnet-4-5-20250929",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
    },
)

response_json = response.json()
llm_output = response_json["choices"][0]["message"]["content"]

# ------------------------------------------
# Step 6: Parse and display the results
# ------------------------------------------
print("\n--- LLM Responses ---\n")
print(llm_output)
