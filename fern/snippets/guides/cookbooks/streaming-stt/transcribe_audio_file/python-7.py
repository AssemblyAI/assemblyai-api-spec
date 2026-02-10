# Configure streaming parameters
streaming_params = StreamingParameters(
    sample_rate=SAMPLE_RATE,
    format_turns=True,
    speech_model="universal-streaming-english",
)

# Store parameters for output file (dynamically capture all set parameters)
session_data["parameters"] = ", ".join(
    f"{k}={v}" for k, v in streaming_params.__dict__.items() if v is not None
)

# Warn if using default turn detection parameters
turn_params = ["end_of_turn_confidence_threshold", "min_end_of_turn_silence_when_confident", "max_turn_silence"]
if not any(getattr(streaming_params, p, None) is not None for p in turn_params):
    print("Warning: Using default turn detection parameters. For best results, fine-tune to your use case:")
    print("https://www.assemblyai.com/docs/universal-streaming/turn-detection#quick-start-configurations\n")

client.connect(streaming_params)
