import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Get transcript using the ID from webhook
transcript = aai.Transcript.get_by_id("<TRANSCRIPT_ID>")

if transcript.status == aai.TranscriptStatus.completed:
    audio_duration = transcript.audio_duration  # Duration in seconds
    # Use audio_duration for billing/tracking
