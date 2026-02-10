# Create the streaming client
client = StreamingClient(
  StreamingClientOptions(
    api_key=YOUR_API_KEY
  )
)

client.on(StreamingEvents.Begin, on_begin)
client.on(StreamingEvents.Turn, on_turn)
client.on(StreamingEvents.Termination, on_terminated)
client.on(StreamingEvents.Error, on_error)
