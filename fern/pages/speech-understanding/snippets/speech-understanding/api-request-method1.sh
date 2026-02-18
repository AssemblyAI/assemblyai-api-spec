curl -X POST \
  "https://api.assemblyai.com/v2/transcript" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://assembly.ai/wildfires.mp3",
    "speaker_labels": true,
    "speech_understanding": {
      "request": {
        "speaker_identification": {
          "speaker_type": "name",
          "known_values": ["Michel Martin", "Peter DeCarlo"]
        }
      }
    }
  }'