import assemblyai as aai

aai.settings.api_key = "AAI_KEY_HERE"


def transcribe(file_url):
    config = aai.TranscriptionConfig(speaker_labels=True)  # Speaker labels must be enabled for this Cookbook.

    transcriber = aai.Transcriber(config=config)

    transcript = transcriber.transcribe(file_url)

    return transcript.json_response
