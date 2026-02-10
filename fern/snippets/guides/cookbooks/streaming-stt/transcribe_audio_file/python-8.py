try:
    client.stream(file_stream)
finally:
    client.disconnect(terminate=True)
    if SAVE_TRANSCRIPT_TO_FILE:
        save_transcript()
