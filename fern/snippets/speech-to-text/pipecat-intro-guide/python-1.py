from pipecat.services.assemblyai.stt import AssemblyAISTTService

# Configure service
stt = AssemblyAISTTService(
    connection_params=AssemblyAIConnectionParams(
        end_of_turn_confidence_threshold=0.4,
        min_end_of_turn_silence_when_confident=400,
        max_turn_silence=1280,
    ),
    api_key=os.getenv("ASSEMBLYAI_API_KEY"),
    vad_force_turn_endpoint=False
)

# Use in pipeline
pipeline = Pipeline([
    transport.input(),
    stt,
    llm,
    ...
])
