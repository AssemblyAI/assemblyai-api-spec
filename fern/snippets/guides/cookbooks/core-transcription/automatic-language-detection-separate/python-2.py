def detect_language(audio_url):
    config = aai.TranscriptionConfig(
        audio_end_at=60000,  # first 60 seconds (in milliseconds)
        language_detection=True,
        speech_model=aai.SpeechModel.nano,
    )
    transcript = transcriber.transcribe(audio_url, config=config)
    return transcript.json_response["language_code"]

def transcribe_file(audio_url, language_code):
    config = aai.TranscriptionConfig(
        language_code=language_code,
        speech_model=(
            aai.SpeechModel.universal
            if language_code in supported_languages_for_universal
            else aai.SpeechModel.nano
        ),
    )
    transcript = transcriber.transcribe(audio_url, config=config)
    return transcript
