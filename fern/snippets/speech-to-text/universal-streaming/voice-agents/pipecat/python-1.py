from pipecat.services.assemblyai.stt import AssemblyAISTTService, AssemblyAIConnectionParams

# Configure service
stt = AssemblyAISTTService(
    api_key=os.getenv("ASSEMBLYAI_API_KEY"),
    vad_force_turn_endpoint=False,  # Use AssemblyAI's STT-based turn detection
    connection_params=AssemblyAIConnectionParams(
        end_of_turn_confidence_threshold=0.4,
        min_end_of_turn_silence_when_confident=400,
        max_turn_silence=1280,
    )
)

# Use in pipeline
pipeline = Pipeline([
    transport.input(),
    stt,
    llm,
    tts,
    transport.output(),
])
