import requests
import time
import json
import re

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

def generate_ner(transcript_text):
    prompt = '''
    You will be given a transcript of a conversation or text. Your task is to generate named entities from the given transcript text.

    Please identify and extract the following named entities from the transcript:

    1. Person names
    2. Organization names
    3. Email addresses
    4. Phone numbers
    5. Full addresses

    When extracting these entities, make sure to return the exact spelling and formatting as they appear in the transcript. Do not modify or standardize the entities in any way.

    Present your results in a JSON format with a single field named "named_entities". This field should contain an array of strings, where each string is a named entity you've identified. For example:
    {
      "named_entities": ["John Doe", "Acme Corp", "john.doe@example.com", "123-456-7890", "123 Main St, Anytown, USA 12345"]
    }

    Important: Do not include any other information, explanations, or text in your response. Your output should consist solely of the JSON object containing the named entities.

    If you do not find any named entities of a particular type, simply return an empty array for the "named_entities" field.
    '''

    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {"role": "user", "content": f"{prompt}\n\nTranscript: {transcript_text}"}
        ],
        "max_tokens": 1000,
        "temperature": 0.0
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()["choices"][0]["message"]["content"]

    try:
        res_json = json.loads(result)
    except:
        res_json = {'named_entities': []}

    named_entities = res_json.get('named_entities', [])
    return named_entities

# Step 1: Transcribe audio
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

# Step 2: Split transcript into sentences and redact PII
transcript_text = transcription_result['text']
sentences = re.split(r'[.!?]+', transcript_text)
redacted_transcript = ''

for sentence in sentences:
    sentence = sentence.strip()
    if not sentence:
        continue

    generated_entities = generate_ner(sentence)
    redacted_sentence = sentence

    for entity in generated_entities:
        redacted_sentence = redacted_sentence.replace(entity, '#' * len(entity))

    redacted_transcript += redacted_sentence + '. '
    print(redacted_sentence)

print('\nFull redacted transcript:')
print(redacted_transcript)
