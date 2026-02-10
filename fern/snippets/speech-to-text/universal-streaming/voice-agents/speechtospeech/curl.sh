curl -X POST https://aaigentsv1.up.railway.app/agents \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "friendly_assistant",
    "instructions": "You are a friendly and helpful assistant. Keep your responses concise and conversational. Be warm and personable.",
    "voice": "luna",
    "greeting": "Say hello and ask how you can help today."
  }'
