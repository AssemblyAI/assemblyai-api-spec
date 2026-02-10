# Include keyterms in connection parameters
keyterms = [
    "AssemblyAI",
    "Universal-Streaming",
    "Baconator",
    "Dr. Rodriguez",
    "iPhone 15 Pro",
    "NASDAQ",
    "PostgreSQL"
]

CONNECTION_PARAMS = {
    "keyterms_prompt": json.dumps(keyterms)  # Up to 100 terms
}

# Build URL with keyterms
API_ENDPOINT = f"{API_ENDPOINT_BASE}?{urlencode(CONNECTION_PARAMS)}"
