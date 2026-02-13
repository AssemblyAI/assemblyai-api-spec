curl -X POST \
  "https://api.assemblyai.com/v2/transcript" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://assembly.ai/wildfires.mp3",
    "speaker_labels": true,
    "language_detection": true,
    "speech_understanding": {
      "request": {
        "translation": {
          "target_languages": ["es", "de"],
          "formal": true
        }
      }
    }
  }'
