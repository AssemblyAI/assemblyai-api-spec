import assemblyai as aai

aai.settings.api_key = "YOUR-API-KEY"
transcriber = aai.Transcriber()

audio_file = (
    "https://assembly.ai/sports_injuries.mp3"
)

config = aai.TranscriptionConfig(speaker_labels=True)
transcript = transcriber.transcribe(audio_file, config)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
    exit(1)

print(transcript.text)

for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")
