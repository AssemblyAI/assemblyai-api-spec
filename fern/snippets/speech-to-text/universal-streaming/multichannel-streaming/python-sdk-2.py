# Connect to streaming service with turn detection configuration
self.client.connect(
    StreamingParameters(
        sample_rate=self.sample_rate,
        format_turns=True,
        end_of_turn_confidence_threshold=0.4,
        min_end_of_turn_silence_when_confident=160,
        max_turn_silence=400,
    )
)
