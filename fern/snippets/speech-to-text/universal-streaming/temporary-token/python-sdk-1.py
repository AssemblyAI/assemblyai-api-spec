client = StreamingClient(
    StreamingClientOptions(
        api_key="<YOUR_API_KEY>",
        api_host="streaming.assemblyai.com",
    )
)

return client.create_temporary_token(expires_in_seconds=60)
