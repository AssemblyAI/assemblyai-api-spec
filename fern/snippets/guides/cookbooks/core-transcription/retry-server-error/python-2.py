def handle_error_transcription(audio_url, transcriber, config, retries=1, wait_time=5):
    for attempt in range(retries + 1):
        transcript = transcriber.transcribe(audio_url, config)
        if transcript.error == "Server error, developers have been alerted":
            if attempt < retries:
                print(f"Encountered a server error. Retrying in {wait_time} second(s)...")
                time.sleep(wait_time)
            else:
                print("Retry failed with a server error. Please contact AssemblyAI Support: support@assemblyai.com")
                return None
        elif transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
            return None
        else:
            return transcript
