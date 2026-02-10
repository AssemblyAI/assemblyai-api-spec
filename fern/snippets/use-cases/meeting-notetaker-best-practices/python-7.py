# Submit job
transcript = transcriber.submit(audio_url, config=config)
print(f"Submitted: {transcript.id}")

# Poll for completion with progress tracking
while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
    await asyncio.sleep(5)
    transcript = transcriber.get_transcript(transcript.id)

    # Optional: Show progress
    print(f"Status: {transcript.status}...")

if transcript.status == aai.TranscriptStatus.completed:
    process_transcript(transcript)
else:
    print(f"Error: {transcript.error}")
