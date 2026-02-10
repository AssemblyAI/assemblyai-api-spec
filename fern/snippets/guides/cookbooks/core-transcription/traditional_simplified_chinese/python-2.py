# Script conversion options:
# - 't2s.json': Traditional to Simplified
# - 's2t.json': Simplified to Traditional

# Create converter object with desired direction
converter = opencc.OpenCC('t2s.json') # For Traditional to Simplified

# Convert the transcript text
simplified_transcript = converter.convert(transcript.text)
