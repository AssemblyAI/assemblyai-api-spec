# STT-based turn detection (recommended)
turn_detection="stt"

stt=assemblyai.STT(
    end_of_turn_confidence_threshold=0.4,
    min_end_of_turn_silence_when_confident=400,  # in ms
    max_turn_silence=1280,  # in ms
)
