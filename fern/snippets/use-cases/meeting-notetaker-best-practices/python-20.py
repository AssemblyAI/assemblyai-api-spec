# Define domain-specific vocabulary
company_terms = [
    "AssemblyAI",
    "Universal-Streaming",
    "Speech Understanding",
    "diarization"
]

participant_names = [
    "Dylan Fox",
    "Sarah Chen",
    "Michael Rodriguez"
]

technical_terms = [
    "API endpoint",
    "WebSocket",
    "latency metrics",
    "TTFT"
]

# Configure with keyterms prompt
config = aai.TranscriptionConfig(
    keyterms_prompt=company_terms + participant_names + technical_terms,
    speaker_labels=True,
    # ... other settings
)
