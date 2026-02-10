import os
from dotenv import load_dotenv
from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import EndFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.runner.utils import parse_telephony_websocket
from pipecat.serializers.telnyx import TelnyxFrameSerializer
from pipecat.services.assemblyai.stt import AssemblyAISTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.deepgram.tts import DeepgramTTSService
from pipecat.transports.websocket.fastapi import (
    FastAPIWebsocketTransport,
    FastAPIWebsocketParams,
)

load_dotenv()

async def run_bot(websocket):
    """Run the voice agent bot with AssemblyAI STT."""

    # Parse Telnyx WebSocket data - automatically extracts call information
    transport_type, call_data = await parse_telephony_websocket(websocket)

    # Extract call information (automatically provided by Telnyx)
    stream_id = call_data["stream_id"]
    call_control_id = call_data["call_control_id"]
    outbound_encoding = call_data["outbound_encoding"]
    from_number = call_data["from"]  # Caller's number
    to_number = call_data["to"]      # Your Telnyx number

    logger.info(f"Incoming call from {from_number} to {to_number}")

    # Create Telnyx serializer with call details
    serializer = TelnyxFrameSerializer(
        stream_id=stream_id,
        call_control_id=call_control_id,
        api_key=os.getenv("TELNYX_API_KEY"),
    )

    # Configure WebSocket transport
    transport = FastAPIWebsocketTransport(
        websocket=websocket,
        params=FastAPIWebsocketParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=False,
            vad_analyzer=SileroVADAnalyzer(),
            serializer=serializer,
        ),
    )

    # Configure AI services
    stt = AssemblyAISTTService(api_key=os.getenv("ASSEMBLYAI_API_KEY"))
    llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    tts = DeepgramTTSService(api_key=os.getenv("DEEPGRAM_API_KEY"))

    # Customize bot behavior based on call information
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful voice assistant. The caller is calling from {from_number}. Keep responses concise and conversational."
        }
    ]

    context = OpenAILLMContext(messages)
    context_aggregator = llm.create_context_aggregator(context)

    # Build pipeline
    pipeline = Pipeline([
        transport.input(),
        stt,
        context_aggregator.user(),
        llm,
        tts,
        transport.output(),
        context_aggregator.assistant(),
    ])

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            allow_interruptions=True,
            audio_in_sample_rate=8000,
            audio_out_sample_rate=8000,
        ),
    )

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Call ended")
        await task.queue_frame(EndFrame())

    # Run the pipeline
    runner = PipelineRunner()
    await runner.run(task)
