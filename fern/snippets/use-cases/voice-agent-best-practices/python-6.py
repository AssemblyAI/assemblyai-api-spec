# Aggressive - Fast customer service
# Best for: IVR, order confirmations, yes/no questions
aggressive_params = {
    "end_of_turn_confidence_threshold": 0.3,  # Lower threshold = faster detection
    "min_end_of_turn_silence_when_confident": 160,  # Less silence needed
    "max_turn_silence": 800  # Quick acoustic fallback
}

# Balanced - Natural conversations (DEFAULT)
# Best for: Customer support, tech support, general conversations
balanced_params = {
    "end_of_turn_confidence_threshold": 0.4,
    "min_end_of_turn_silence_when_confident": 400,
    "max_turn_silence": 1280
}

# Conservative - Medical dictation, complex instructions
# Best for: Healthcare, legal, detailed technical support
conservative_params = {
    "end_of_turn_confidence_threshold": 0.5,  # Higher threshold = more patient
    "min_end_of_turn_silence_when_confident": 560,  # More silence before confirming
    "max_turn_silence": 2000  # Longer acoustic fallback
}
