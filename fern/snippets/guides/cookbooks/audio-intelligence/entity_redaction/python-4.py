# filter for some entities
redacted_transcript2 = transcript.text

pii_policies = ["location"]

for entity in transcript.entities:
    if entity.entity_type in pii_policies:
        redacted_transcript2 = redacted_transcript2.replace(entity.text, f"[{entity.entity_type.upper()}]")

print(redacted_transcript2[:500])
