# Step 1: Submit transcription job
curl -X POST "https://api.assemblyai.com/v2/transcript" \
  -H "authorization: <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://assembly.ai/wildfires.mp3",
    "speaker_labels": true
  }'

# Save the transcript_id from the response above, then use it in the following commands

# Step 2: Poll for transcription status (repeat until status is "completed")
curl -X GET "https://api.assemblyai.com/v2/transcript/{transcript_id}" \
  -H "authorization: <YOUR_API_KEY>"

# Step 3: Once transcription is completed, enable speaker identification
curl -X POST "https://llm-gateway.assemblyai.com/v1/understanding" \
  -H "authorization: <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "transcript_id": "{transcript_id}",
    "speech_understanding": {
      "request": {
        "speaker_identification": {
          "speaker_type": "name",
          "known_values": ["Michel Martin", "Peter DeCarlo"]
        }
      }
    }
  }'