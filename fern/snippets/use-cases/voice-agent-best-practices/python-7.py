# Use VAD-only mode (silence-based only)
params = {"end_of_turn_confidence_threshold": 1.0}

# Use an external turn detection model (fastest possible)
params = {"end_of_turn_confidence_threshold": 0.01}
