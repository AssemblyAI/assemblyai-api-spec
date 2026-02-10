from pipecat.services.assemblyai import AssemblyAISTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.rime import RimeTTSService

# Configure services
stt = AssemblyAISTTService(
    api_key="your_key",
    connection_params=AssemblyAIConnectionParams(
        end_of_turn_confidence_threshold=0.4,
        min_end_of_turn_silence_when_confident=160,  # ms after confident EOT
        format_turns=False  # CRITICAL: Faster without formatting
    ),
    vad_force_turn_endpoint=False,  # Rely on AssemblyAI's EOT, not VAD
)
llm = OpenAILLMService(api_key="your_key")
tts = RimeTTSService(api_key="your_key")
