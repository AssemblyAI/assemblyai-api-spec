import requests
import time

base_url = "https://api.assemblyai.com"

headers = {
  "authorization": "YOUR_API_KEY"
}

audio_url = "https://assembly.ai/wildfires.mp3"

# Configure transcription with translation and speaker labels
data = {
  "audio_url": audio_url,
  "speaker_labels": True,  # Enable speaker labels
  # "language_detection": True,  # Enable language detection if you are processing files in a variety of languages
  "speech_understanding": {
    "request": {
      "translation": {
        "target_languages": ["es"],
        "match_original_utterance": True,  # Get translated text per utterance
        "formal": True
      }
    }
  }
}

# Submit transcription request
response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

# Poll transcription results
while True:
  transcript = requests.get(polling_endpoint, headers=headers).json()

  if transcript["status"] == "completed":
    break

  elif transcript["status"] == "error":
    raise RuntimeError(f"Transcription failed: {transcript['error']}")

  else:
    time.sleep(3)

# Access translated utterances
for utterance in transcript["utterances"]:
  print(f"Speaker {utterance['speaker']}:")
  print(f"  Original: {utterance['text'][:100]}...")
  print(f"  Spanish: {utterance['translated_texts']['es'][:100]}...")
  print()
