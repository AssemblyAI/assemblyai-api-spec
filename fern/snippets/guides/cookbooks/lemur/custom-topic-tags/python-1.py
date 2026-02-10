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

# Step 2: Generate topic tags with LLM Gateway
tag_list = {
    'Sports': 'News and updates on various athletic events, teams, and sports personalities.',
    'Politics': 'Coverage and discussion of government activities, policies, and political events.',
    'Entertainment': 'Information on movies, music, television, celebrities, and arts.',
    'Technology': 'News and reviews on gadgets, software, tech advancements, and trends.',
    'Health': 'Articles focusing on medical news, wellness, and health-related topics.',
    'Business': 'Updates on markets, industries, companies, and economic trends.',
    'Science': 'News and insights into scientific discoveries, research, and innovations.',
    'Education': 'Coverage of topics related to schools, educational policies, and learning.',
    'Travel': 'Information on destinations, travel tips, and tourism news.',
    'Lifestyle': 'Articles on fashion, hobbies, personal interests, and daily life.',
    'Environment': 'News and discussion about environmental issues and sustainability.',
    'Finance': 'Information on personal finance, investments, banking, and economic news.',
    'World News': 'International news covering global events and issues.',
    'Crime': 'Reports and updates on criminal activities, law enforcement, and legal cases.',
    'Culture': 'Coverage of cultural events, traditions, and societal norms.'
}

prompt = f"""
You are a helpful assistant designed to label video content with topic tags.

I will give you a list of topics and definitions. Select the most relevant topic from the list. Return your selection and nothing else.

<topics_list>
{tag_list}
</topics_list>
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
print(result.strip())
