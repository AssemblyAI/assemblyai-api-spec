# Main execution
# If using a local file:
audio_url = upload_file("<YOUR_AUDIO FILE>")

# If using a public URL:
# audio_url = "<YOUR_AUDIO_URL>"

# Transcribe audio
transcript = transcribe_audio(audio_url)
transcript_text = transcript["text"]
transcript_id = transcript["id"]

# Get sentences
print("Getting sentences...")
sentences = get_sentences(transcript_id)
