from pipecat.services.assemblyai.stt import AssemblyAISTTService, AssemblyAIConnectionParams

# Configure AssemblyAI with custom parameters
stt_params = AssemblyAIConnectionParams(
    sample_rate=8000,
    end_of_turn_confidence_threshold=0.4,
    min_end_of_turn_silence_when_confident=400,
    max_turn_silence=1280,
    keyterms_prompt=["NPI", "TIN", "CMS", "PTAN", "CPT", "CDT", "DOB", "SSN"]
)

stt = AssemblyAISTTService(
    api_key=os.getenv("ASSEMBLYAI_API_KEY"),
    connection_params=stt_params,
)
