import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Step 1: Transcribe and get paragraphs
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

# Get paragraphs
paragraphs = requests.get(polling_endpoint + '/paragraphs', headers=headers).json()['paragraphs']

# Step 2: Combine paragraphs and create chapter summaries
combined_paragraphs = []
step = 2  # Adjust as needed if you want combined paragraphs to be shorter or longer in length.

# Combine paragraphs into groups, finding the appropriate timestamps and combining all their text into one string.
for i in range(0, len(paragraphs), step):
    paragraph_group = paragraphs[i : i + step]
    start = paragraph_group[0]['start']
    end = paragraph_group[-1]['end']
    text = ""
    for paragraph in paragraph_group:
        text += f"{paragraph['text']} "
    combined_paragraphs.append(f"Paragraph: {text} Start: {start} End: {end}")

results = []

# Step 3: Generate summaries with LLM Gateway
for paragraph in combined_paragraphs:
    prompt = "Summarize this text as a whole and provide start and end timestamps."

    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {"role": "user", "content": f"{prompt}\n\n{paragraph}"}
        ],
        "max_tokens": 1000
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()["choices"][0]["message"]["content"]
    results.append(result)

for result in results:
    print(f"{result}\n")
