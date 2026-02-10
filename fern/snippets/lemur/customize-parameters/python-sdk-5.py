transcript_group = transcriber.transcribe_group(
    [
        "https://example.org/customer1.mp3",
        "https://example.org/customer2.mp3",
        "https://example.org/customer3.mp3",
    ],
)

# Or use existing transcripts:
# transcript_group = aai.TranscriptGroup.get_by_ids([id1, id2, id3])

result = transcript_group.lemur.task(
  prompt="Provide a summary of these customer calls."
)
