curl https://api.assemblyai.com/v2/transcript \
--header "Authorization: <YOUR_API_KEY>" \
--header "Content-Type: application/json" \
--data '{
  "audio_url": "YOUR_AUDIO_URL",
  "speech_model": "universal-3-pro",
  "language_detection": true,
  "speaker_labels": true,
  "speakers_expected": 3
}'
