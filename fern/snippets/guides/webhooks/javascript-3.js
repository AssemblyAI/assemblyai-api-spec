client.transcripts.submit({
  audio:
    'https://assembly.ai/wildfires.mp3',
  webhook_url: 'https://example.com/webhook'
  webhook_auth_header_name: "X-My-Webhook-Secret",
  webhook_auth_header_value: "secret-value"
})
