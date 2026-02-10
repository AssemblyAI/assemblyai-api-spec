def transcribe_audio(audio_file):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(os.path.join(batch_folder, audio_file))
    if transcript.status == "completed":
        with open(f"{transcription_result_folder}/{audio_file}.txt", "w") as f:
            f.write(transcript.text)
    elif transcript.status == "error":
        print("Error: ", transcript.error)
