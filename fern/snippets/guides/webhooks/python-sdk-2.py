import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

transcript = aai.Transcript.get_by_id("<TRANSCRIPT_ID>")

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)
