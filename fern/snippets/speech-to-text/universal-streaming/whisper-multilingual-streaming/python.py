import websockets
import asyncio
import json
from urllib.parse import urlencode

import pyaudio

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

BASE_URL = "wss://streaming.assemblyai.com/v3/ws"
CONNECTION_PARAMS = {
    "sample_rate": RATE,
    "speech_model": "whisper-streaming",
    "language_detection": True,
}
URL = f"{BASE_URL}?{urlencode(CONNECTION_PARAMS)}"

async def send_receive():

    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(
        URL,
        additional_headers={"Authorization": "YOUR-API-KEY"},
        ping_interval=5,
        ping_timeout=20
    ) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    await _ws.send(data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                except Exception as e:
                    print(e)
                await asyncio.sleep(0.01)

        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    data = json.loads(result_str)
                    transcript = data['transcript']
                    utterance = data['utterance']

                    if data['type'] == 'Turn':
                        if not data.get('end_of_turn') and transcript:
                            print(f"[PARTIAL TURN TRANSCRIPT]: {transcript}")
                        if data.get('utterance'):
                            print(f"[PARTIAL TURN UTTERANCE]: {utterance}")
                            # Display language detection info if available
                            if 'language_code' in data:
                                print(f"[UTTERANCE LANGUAGE DETECTION]: {data['language_code']} - {data['language_confidence']:.2%}")
                        if data.get('end_of_turn'):
                            print(f"[FULL TURN TRANSCRIPT]: {transcript}")
                            # Display language detection info if available
                            if 'language_code' in data:
                                print(f"[END OF TURN LANGUAGE DETECTION]: {data['language_code']} - {data['language_confidence']:.2%}")
                    else:
                        pass

                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    print(f"\nError receiving data: {e}")
                    break

        try:
            await asyncio.gather(send(), receive())
        except KeyboardInterrupt:
            await _ws.send({"type": "Terminate"})
            # Wait for the server to close the connection after receiving the message
            await _ws.wait_closed()
            print("Session terminated and connection closed.")

if __name__ == "__main__":
    try:
        asyncio.run(send_receive())
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
