import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
  "authorization": "<YOUR_API_KEY>"
}

# Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
audio_url = "https://assembly.ai/wildfires.mp3"

# Submit transcription request (without translation)
data = {
  "audio_url": audio_url,
  "speech_models": ["universal-3-pro", "universal-2"],
  "language_detection": True,
  "speaker_labels": True,
}

# Transcribe file
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

# Add translation configuration to the completed transcript
understanding_body = {
  "transcript_id": transcript_id,
  "speech_understanding": {
    "request": {
      "translation": {
      "target_languages": ["es", "de"],  # Translate to Spanish and German
      "formal": True  # Use formal language style
      }
    }
  }
}

# Send to Speech Understanding API for translation
result = requests.post(
  "https://llm-gateway.assemblyai.com/v1/understanding",
  headers=headers,
  json=understanding_body
).json()

# Access and display results
print("\n--- Original Transcript ---")
print(transcript['text'][:200] + "...\n")

print("--- Translations ---")
for language_code, translated_text in result['translated_texts'].items():
  print(f"{language_code.upper()}:")
  print(translated_text[:200] + "...\n")
