from livekit.plugins import assemblyai

session = AgentSession(
    stt = assemblyai.STT(
      end_of_turn_confidence_threshold=0.4,
      min_end_of_turn_silence_when_confident=400,
      max_turn_silence=1280,
    ),
    # ... llm, tts, etc.
    vad=silero.VAD.load(), # VAD Enabled for Interruptions
    turn_detection="stt", # Enable Turn Detection
)
