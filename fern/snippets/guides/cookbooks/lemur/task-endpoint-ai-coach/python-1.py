import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "<YOUR_API_KEY>"}

# Use a publicly-accessible URL:
audio_url = "https://storage.googleapis.com/aai-web-samples/meeting.mp4"

# with open("/your_audio_file.mp3", "rb") as f:
#     response = requests.post(base_url + "/v2/upload", headers=headers, data=f)
#     if response.status_code != 200:
#         print(f"Error: {response.status_code}, Response: {response.text}")
#         response.raise_for_status()
#     upload_json = response.json()
#     audio_url = upload_json["upload_url"]

data = {
    "audio_url": audio_url,
}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)

if response.status_code != 200:
    print(f"Error: {response.status_code}, Response: {response.text}")

transcript_json = response.json()
transcript_id = transcript_json["id"]
polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()
    if transcript["status"] == "completed":
        print(transcript['id'])
        print(f" \nFull Transcript: \n\n{transcript['text']}\n")

        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    else:
        time.sleep(3)

prompt = f"""
        - You are an expert at providing valuable feedback to individuals.
        - You possess exceptionally high emotional intelligence.
        - You excel at analyzing the behavior of individuals in the given transcript and providing insights on how they could improve.
        - You emphasize constructive criticism in your feedback.
        - The feedback focuses on how people can better achieve their objectives.
        - You avoid providing unjustified or unfounded feedback.
        - Your communication is clear, accurate and concise, and you write with perfect English.
        - Directly start with the feedback without any preamble or introduction.
        """

llm_gateway_data = {
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
      {
        "role": "user",
        "content": f"{prompt} Please provide feedback for this transcript: \n\n{transcript["text"]}"
      }
    ],
    "max_tokens": 1500
  }

response = requests.post(
  "https://llm-gateway.assemblyai.com/v1/chat/completions",
  headers=headers,
  json=llm_gateway_data
)

result = response.json()

if "error" in result:
    print(f"\nError from LLM Gateway: {result['error']}")
else:
    response_text = result['choices'][0]['message']['content']
    print(f"\nResponse ID: {result["request_id"]}\n")
    print(response_text)
