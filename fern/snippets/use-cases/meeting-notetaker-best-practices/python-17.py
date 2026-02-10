# Extract all organizations mentioned
organizations = [
    entity.text for entity in transcript.entities
    if entity.entity_type == "organization"
]
print(f"Companies mentioned: {', '.join(organizations)}")
