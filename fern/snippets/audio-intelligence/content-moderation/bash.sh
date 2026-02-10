curl https://api.assemblyai.com/v2/transcript \
--header "Authorization: <YOUR_API_KEY>" \
--header "Content-Type: application/json" \
--data '{
  "audio_url": "YOUR_AUDIO_URL",
  "content_safety": true,
  "content_safety_confidence": 60
}'
