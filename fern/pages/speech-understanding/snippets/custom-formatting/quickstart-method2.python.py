import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
  "authorization": "<YOUR_API_KEY>"
}

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/phone-msg.m4a"

# Submit transcription request (without formatting)
data = {
  "audio_url": audio_url,
  "speech_models": ["universal-3-pro", "universal-2"],
  "language_detection": True,
  "speaker_labels": True
}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

# Poll for transcription completion
while True:
  transcript = requests.get(polling_endpoint, headers=headers).json()

  if transcript["status"] == "completed":
    print("Transcription completed!")
    break

  elif transcript["status"] == "error":
    raise RuntimeError(f"Transcription failed: {transcript['error']}")

  else:
    time.sleep(3)

# Add custom formatting configuration to the completed transcript
understanding_body = {
  "transcript_id": transcript_id,
  "speech_understanding": {
    "request": {
      "custom_formatting": {
      "date": "mm/dd/yyyy",
      "phone_number": "(xxx)xxx-xxxx",
      "email": "username@domain.com",
      "format_utterances": True
      }
    }
  }
}

# Send to Speech Understanding API for formatting
result = requests.post(
  "https://llm-gateway.assemblyai.com/v1/understanding",
  headers=headers,
  json=understanding_body
).json()

print("Formatting completed!")

# Access and display results
print("\n--- Formatting Details ---")
mapping = result['speech_understanding']['response']['custom_formatting']['mapping']
for original, formatted in mapping.items():
  print(f"Original: {original}")
  print(f"Formatted: {formatted}\n")
