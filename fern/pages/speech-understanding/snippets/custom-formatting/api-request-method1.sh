curl -X POST \
  "https://api.assemblyai.com/v2/transcript" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://assembly.ai/phone-msg.m4a",
    "speaker_labels": true,
    "speech_understanding": {
      "request": {
        "custom_formatting": {
          "date": "mm/dd/yyyy",
          "phone_number": "(xxx)xxx-xxxx",
          "email": "username@domain.com",
          "format_utterances": true
        }
      }
    }
  }'
