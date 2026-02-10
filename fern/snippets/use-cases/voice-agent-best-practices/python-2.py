# LiveKit + AssemblyAI Quick Start
from livekit import agents
from livekit.plugins import assemblyai, openai, rime

async def create_voice_agent():
    # Initialize AssemblyAI STT
    stt = assemblyai.STT(
        api_key="your_assemblyai_key",
        end_of_turn_confidence_threshold=0.4,
        min_end_of_turn_silence_when_confident=160,
        format_turns=False  # CRITICAL: Faster without formatting
    )

    # Add LLM
    llm = openai.LLM(api_key="your_openai_key")

    # Add TTS
    tts = rime.TTS(api_key="your_rime_key")

    # Create agent
    agent = agents.VoiceAssistant(
        stt=stt,
        llm=llm,
        tts=tts,
        turn_detection="stt"  # Use AssemblyAI's turn detection
    )

    return agent
