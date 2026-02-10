redacted_transcript = transcript.text

# redact ALL entities
for entity in transcript.entities:
    redacted_transcript = redacted_transcript.replace(entity.text, f"[{entity.entity_type.upper()}]")

print(redacted_transcript[:500])
