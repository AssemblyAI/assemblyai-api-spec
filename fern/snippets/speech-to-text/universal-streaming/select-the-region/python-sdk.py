import assemblyai as aai
from assemblyai.streaming.v3 import StreamingClient, StreamingClientOptions

api_key = "<YOUR_API_KEY>"

client = StreamingClient(
    StreamingClientOptions(
        api_key=api_key,
        api_host="streaming.eu.assemblyai.com",
    )
)

client.connect()
client.stream(aai.extras.MicrophoneStream(sample_rate=16000))
