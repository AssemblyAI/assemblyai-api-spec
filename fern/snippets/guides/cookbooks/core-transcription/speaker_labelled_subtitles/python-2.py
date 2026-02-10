import assemblyai as aai

# SETTINGS
aai.settings.api_key = "YOUR-API-KEY"
filename = "YOUR-FILE-NAME"
transcriber = aai.Transcriber(config=aai.TranscriptionConfig(speaker_labels=True))
transcript = transcriber.transcribe(filename)

# Maximum number of words per subtitle
max_words_per_subtitle = 6
