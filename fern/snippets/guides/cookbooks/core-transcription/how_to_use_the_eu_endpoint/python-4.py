import assemblyai as aai
from assemblyai.streaming.v3 import StreamingClient, StreamingClientOptions

client = StreamingClient(
    StreamingClientOptions(
        api_key="YOUR_API_KEY",
        api_host="streaming.eu.assemblyai.com"  # EU streaming endpoint
    )
)
