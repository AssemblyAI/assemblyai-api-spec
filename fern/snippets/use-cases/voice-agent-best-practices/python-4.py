# Maximum speed configuration
latency_optimized_params = {
    "sample_rate": 16000,
    "encoding": "pcm_s16le",

    # CRITICAL latency optimizations
    "format_turns": False,  # NEVER use for voice agents - saves ~200ms

    # Aggressive turn detection for quick responses
    "end_of_turn_confidence_threshold": 0.4,  # Lower = faster detection
    "min_end_of_turn_silence_when_confident": 160,  # Minimal silence required
    "max_turn_silence": 800,  # Faster fallback

    # Audio optimization
    "chunk_size": 512  # Smaller chunks = lower latency
}
