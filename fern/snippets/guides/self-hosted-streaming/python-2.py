import asyncio
import websockets
import pyaudio
import json

# Replace with your server's IP address or use 'localhost' for local testing
SERVER_IP = "your.server.ip.address"

async def stream_audio(language="en"):
    # Build WebSocket URL with query parameters
    params = f"sample_rate=16000&language={language}"
    WS_URL = f"ws://{SERVER_IP}:8080/v3/ws?{params}"

    # Add authorization header (required for self-hosted)
    headers = {"Authorization": "self-hosted"}

    print(f"Connecting to {WS_URL}...")

    async with websockets.connect(WS_URL, extra_headers=headers) as ws:
        print("Connected! Starting to stream audio...")

        # Set up audio stream from microphone
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=3200  # 100ms chunks at 16kHz
        )

        print(f"\n🎤 Listening with language={language}... speak into your microphone!")
        print("Press Ctrl+C to stop\n")

        # Function to send audio
        async def send_audio():
            try:
                while True:
                    data = stream.read(3200, exception_on_overflow=False)
                    await ws.send(data)
                    await asyncio.sleep(0.1)  # 100ms chunks
            except KeyboardInterrupt:
                await ws.send(json.dumps({"type": "Terminate"}))
                print("\nStopping...")
            finally:
                stream.stop_stream()
                stream.close()
                p.terminate()

        # Function to receive transcripts
        async def receive_transcripts():
            try:
                async for message in ws:
                    data = json.loads(message)

                    if data.get("type") == "Begin":
                        print(f"✅ Session started! ID: {data.get('id')}")

                    elif data.get("type") == "Turn":
                        if data.get("words"):
                            text = " ".join([word["text"] for word in data["words"]])
                            end_of_turn = "[FINAL]" if data.get("end_of_turn") else ""
                            print(f"📝 {text} {end_of_turn}")

                    elif data.get("type") == "Termination":
                        print(f"✅ Session completed. Duration: {data.get('session_duration_seconds')}s")
                        break

            except Exception as e:
                print(f"Error receiving: {e}")

        # Run both tasks concurrently
        await asyncio.gather(send_audio(), receive_transcripts())

if __name__ == "__main__":
    import sys

    # Usage: python live_microphone_streaming.py [language]
    # Examples:
    #   python live_microphone_streaming.py en       # English
    #   python live_microphone_streaming.py multi    # Multilingual with auto-detect
    #   python live_microphone_streaming.py es       # Spanish
    language = sys.argv[1] if len(sys.argv) > 1 else "en"

    try:
        asyncio.run(stream_audio(language))
    except KeyboardInterrupt:
        print("\nStopped by user")
