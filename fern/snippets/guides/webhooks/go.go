client.Transcripts.SubmitFromURL(ctx, audioURL, &aai.TranscriptOptionalParams{
    WebhookURL:             aai.String("https://example.com/webhook"),
    WebhookAuthHeaderName:  aai.String("X-My-Webhook-Secret"),
    WebhookAuthHeaderValue: aai.String("secret-value"),
})
