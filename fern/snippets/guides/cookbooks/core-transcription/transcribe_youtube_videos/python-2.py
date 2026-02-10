import assemblyai as aai

aai.settings.api_key = "YOUR_API_KEY"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("wtolixa9XTg.m4a")
print(transcript.text)
