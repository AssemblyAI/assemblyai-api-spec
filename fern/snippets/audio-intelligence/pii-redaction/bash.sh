curl https://api.assemblyai.com/v2/transcript \
--header "Authorization: <YOUR_API_KEY>" \
--header "Content-Type: application/json" \
--data '{
  "audio_url": "YOUR_AUDIO_URL",
  "redact_pii": true,
  "redact_pii_policies": ["us_social_security_number", "credit_card_number"],
  "redact_pii_sub": "hash",
  "redact_pii_audio": true,
  "redact_pii_audio_quality": "mp3"
}'
