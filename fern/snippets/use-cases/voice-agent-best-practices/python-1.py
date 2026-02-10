import asyncio
import json
import websockets
from urllib.parse import urlencode
import pyaudio
import threading
from queue import Queue

# Configuration
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your AssemblyAI API key
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024

# WebSocket connection parameters
CONNECTION_PARAMS = {
    "sample_rate": SAMPLE_RATE,
    "format_turns": False,  # CRITICAL: Unformatted for fastest response (~200ms savings)
    "end_of_turn_confidence_threshold": 0.4,  # Balanced turn detection
    "min_end_of_turn_silence_when_confident": 160,  # ms after confident EOT
    "max_turn_silence": 1280  # Acoustic fallback threshold
}

# Build WebSocket URL
API_ENDPOINT_BASE = "wss://streaming.assemblyai.com/v3/ws"
API_ENDPOINT = f"{API_ENDPOINT_BASE}?{urlencode(CONNECTION_PARAMS)}"

# Audio queue for thread-safe audio handling
audio_queue = Queue()

def audio_callback(in_data, frame_count, time_info, status):
    """Callback for audio stream - adds audio to queue"""
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

async def send_audio(websocket):
    """Send audio data to WebSocket"""
    print("📤 Starting audio sender...")
    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            await websocket.send(audio_data)
        else:
            await asyncio.sleep(0.01)

async def receive_transcripts(websocket):
    """Receive and log all transcripts"""
    print("📥 Starting transcript receiver...")
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)

            # Log complete JSON response
            print("\n" + "="*50)
            print("📝 RECEIVED MESSAGE:")
            print(json.dumps(data, indent=2))

            # Highlight important fields
            if data.get("type") == "Turn":
                print("\n🔍 KEY FIELDS:")
                print(f"  Turn Order: {data.get('turn_order')}")
                print(f"  Transcript: '{data.get('transcript')}'")
                print(f"  End of Turn: {data.get('end_of_turn')}")
                print(f"  EOT Confidence: {data.get('end_of_turn_confidence', 0):.3f}")
                print(f"  Utterance: {data.get('utterance')}")

                # KEY INSIGHT: Utterance field enables pre-emptive generation
                if data.get("utterance"):
                    print("\n✅ UTTERANCE AVAILABLE - Ready for LLM processing!")
                    print("   💡 Start generating LLM response now, don't wait for end_of_turn")

                # KEY INSIGHT: end_of_turn signals when to respond
                if data.get("end_of_turn"):
                    print("\n🎯 END OF TURN - User finished speaking, agent can respond")

        except websockets.exceptions.ConnectionClosed:
            print("❌ Connection closed")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """Main function to coordinate streaming"""
    print("🚀 Universal-Streaming Terminal Logger")
    print(f"📡 Connecting to: {API_ENDPOINT_BASE}")
    print(f"🔧 Configuration: {json.dumps(CONNECTION_PARAMS, indent=2)}")
    print("-" * 50)

    # Set up audio stream
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
        stream_callback=audio_callback
    )

    # Connect to WebSocket with auth header
    headers = {"Authorization": API_KEY}

    try:
        # If you're using `websockets` version 13.0 or later, use `additional_headers` parameter. For older versions (< 13.0), use `extra_headers` instead.
        async with websockets.connect(API_ENDPOINT, additional_headers=headers) as websocket:
            print("✅ Connected to Universal-Streaming!")
            print("🎤 Start speaking... (Press Ctrl+C to stop)\n")

            # Start audio stream
            stream.start_stream()

            # Run send and receive concurrently
            await asyncio.gather(
                send_audio(websocket),
                receive_transcripts(websocket)
            )

    except KeyboardInterrupt:
        print("\n👋 Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("✅ Cleaned up resources")

if __name__ == "__main__":
    asyncio.run(main())
