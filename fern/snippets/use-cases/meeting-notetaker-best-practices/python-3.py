config = aai.TranscriptionConfig(
    multichannel=True,  # Enable when each speaker is on different channel
    speaker_labels=False,  # Disable - channels already separate speakers
    # Other settings...
)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_file, config=config)

# Access per-channel transcripts
for channel, channel_transcript in enumerate(transcript.channels):
    print(f"\n=== Channel {channel} ===")
    print(channel_transcript.text)
