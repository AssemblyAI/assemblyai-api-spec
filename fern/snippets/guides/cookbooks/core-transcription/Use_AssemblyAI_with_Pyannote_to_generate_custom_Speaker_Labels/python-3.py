def transcribe_audio(audio_file, language="en"):
    """
    Transcribe an audio file using AssemblyAI.

    Args:
        audio_file (str): Path to the audio file.
        language (str, optional): Language code for transcription. Defaults to "en".

    Returns:
        aai.Transcript: The transcription result.
    """

    transcriber = aai.Transcriber(config=aai.TranscriptionConfig(speech_model='nano', language_code=language))
    transcript = transcriber.transcribe(audio_file)
    print(f"Transcript ID: {transcript.id}")
    return transcript
