import assemblyai as aai
aai.settings.api_key = "YOUR_API_KEY"
transcriber = aai.Transcriber()

def transcribe(urls):
    return transcriber.transcribe_group(urls)
