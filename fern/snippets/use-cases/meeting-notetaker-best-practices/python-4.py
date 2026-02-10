import asyncio
import websockets

class ChannelTranscriber:
    def __init__(self, channel_id: int, speaker_name: str):
        self.channel_id = channel_id
        self.speaker_name = speaker_name
        self.connection_params = {
            "sample_rate": 16000,
            "format_turns": True,
        }

    async def transcribe_channel(self, audio_stream):
        """Transcribe a single audio channel"""
        url = f"wss://streaming.assemblyai.com/v3/ws?{urlencode(self.connection_params)}"

        # If you're using `websockets` version 13.0 or later, use `additional_headers` parameter. For older versions (< 13.0), use `extra_headers` instead.
        async with websockets.connect(url, additional_headers={"Authorization": API_KEY}) as ws:
            # Send audio from this channel only
            async for audio_chunk in audio_stream:
                await ws.send(audio_chunk)

            # Receive transcripts
            async for message in ws:
                data = json.loads(message)
                if data.get("type") == "Turn" and data.get("turn_is_formatted"):
                    print(f"{self.speaker_name}: {data['transcript']}")

# Create transcriber for each channel
async def transcribe_multichannel_meeting(channel_audio_streams):
    transcribers = [
        ChannelTranscriber(0, "Alice"),
        ChannelTranscriber(1, "Bob"),
    ]

    # Run all channels concurrently
    await asyncio.gather(*[
        t.transcribe_channel(stream)
        for t, stream in zip(transcribers, channel_audio_streams)
    ])
