import assemblyai as aai

aai.settings.base_url = "https://api.assemblyai.com"
aai.settings.api_key = "YOUR_API_KEY"

# Use a publicly-accessible URL
audio_file = "https://assembly.ai/wildfires.mp3"

# Or use a local file:
# audio_file = "./example.mp3"

config = aai.TranscriptionConfig(
    speech_models=["universal-3-pro", "universal-2"],
    language_detection=True,
    speaker_labels=True,
)

transcript = aai.Transcriber().transcribe(audio_file, config=config)

if transcript.status == aai.TranscriptStatus.error:
    raise RuntimeError(f"Transcription failed: {transcript.error}")

print(f"\nFull Transcript:\n\n{transcript.text}")

# Optionally print speaker diarization results
# for utterance in transcript.utterances:
#     print(f"Speaker {utterance.speaker}: {utterance.text}")
