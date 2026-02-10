# Streaming with contextual keyterms
keyterms = [
    # Participant names
    "Alice Johnson",
    "Bob Smith",

    # Meeting-specific vocabulary
    "Q4 objectives",
    "revenue targets",
    "customer acquisition",

    # Technical terms
    "API integration",
    "cloud migration"
]

CONNECTION_PARAMS = {
    "sample_rate": 16000,
    "format_turns": True,
    "keyterms_prompt": json.dumps(keyterms),  # JSON-encode for URL params
}
