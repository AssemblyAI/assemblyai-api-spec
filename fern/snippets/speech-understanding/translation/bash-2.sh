# Step 1: Get the completed transcript
transcript=$(curl -s -X GET \
  "https://api.assemblyai.com/v2/transcript/YOUR_TRANSCRIPT_ID" \
  -H "Authorization: YOUR_API_KEY")

# Step 2: Add translation and send to Speech Understanding API
curl -X POST \
  "https://llm-gateway.assemblyai.com/v1/understanding" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "transcript_id": "{transcript_id}",
    "speech_understanding": {
      "request": {
        "translation": {
          "target_languages": ["es", "de"],
          "formal": true
        }
      }
    }
  }'
