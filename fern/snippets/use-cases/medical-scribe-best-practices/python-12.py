# Streaming with medical context and post-processing
medical_terms = [
    # Patient-specific history
    "coronary artery disease",
    "CABG in 2019",
    "ejection fraction 45%",

    # Current visit context
    "chest pain",
    "shortness of breath",
    "orthopnea",

    # Likely medications
    "carvedilol",
    "furosemide",
    "spironolactone"
]

transcriber = aai.RealtimeTranscriber(
    sample_rate=16000,
    format_turns=True,
    key_terms=medical_terms,
    on_data=lambda transcript: post_process_medical(transcript)
)

def post_process_medical(transcript):
    """Apply LLM correction for medical context"""
    # Send to LLM Gateway for medical terminology correction
    # This improves contextual accuracy significantly
    corrected = llm_gateway.correct_medical(transcript.text)
    return corrected
