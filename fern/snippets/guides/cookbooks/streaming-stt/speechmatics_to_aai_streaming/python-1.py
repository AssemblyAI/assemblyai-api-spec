import pyaudio
import websocket
import json
import threading
import time

# --- Configuration ---

YOUR_API_KEY = "YOUR-API-KEY" # Replace with your actual API key

CONNECTION_PARAMS = {
"language": "en",
"enable_partials": True,
"max_delay": 2.0
}
API_ENDPOINT = "wss://eu2.rt.speechmatics.com/v2/en"

# Audio Configuration

FRAMES_PER_BUFFER = 1024 # Chunk size
SAMPLE_RATE = None # Will be set based on device capabilities
CHANNELS = 1
FORMAT = pyaudio.paFloat32 # Speechmatics uses float32 format

# Global variables for audio stream and websocket

audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event() # To signal the audio thread to stop
audio_seq_no = 0 # Track number of audio chunks sent

# --- WebSocket Event Handlers ---

def on_open(ws):
"""Called when the WebSocket connection is established."""
print("WebSocket connection opened.")
print(f"Connected to: {API_ENDPOINT}")

    # Send StartRecognition message
    start_message = {
        "message": "StartRecognition",
        "audio_format": {
            "type": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": SAMPLE_RATE
        },
        "transcription_config": {
            "language": CONNECTION_PARAMS["language"],
            "enable_partials": CONNECTION_PARAMS["enable_partials"],
            "max_delay": CONNECTION_PARAMS["max_delay"]
        }
    }
    ws.send(json.dumps(start_message))

def on_message(ws, message):
global audio_seq_no

    try:
        data = json.loads(message)
        msg_type = data.get('message')

        if msg_type == "RecognitionStarted":
            session_id = data.get('id')
            print(f"\nSession began: ID={session_id}")

            # Start sending audio data in a separate thread
            def stream_audio():
                global audio_seq_no, stream
                print("Starting audio streaming...")
                while not stop_event.is_set():
                    try:
                        audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                        # Send audio data as binary message
                        ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
                        audio_seq_no += 1
                    except Exception as e:
                        print(f"Error streaming audio: {e}")
                        # If stream read fails, likely means it's closed, stop the loop
                        break
                print("Audio streaming stopped.")

            global audio_thread
            audio_thread = threading.Thread(target=stream_audio)
            audio_thread.daemon = (
                True  # Allow main thread to exit even if this thread is running
            )
            audio_thread.start()

        elif msg_type == "AddPartialTranscript":
            transcript = data.get('metadata', {}).get('transcript', '')
            if transcript:
                print(f"\r{transcript}", end='')

        elif msg_type == "AddTranscript":
            transcript = data.get('metadata', {}).get('transcript', '')
            if transcript:
                # Clear previous line for final messages
                print('\r' + ' ' * 80 + '\r', end='')
                print(transcript)

        elif msg_type == "EndOfTranscript":
            print("\nSession Terminated: Transcription complete")

        elif msg_type == "Error":
            error_type = data.get('type')
            reason = data.get('reason')
            print(f"\nWebSocket Error: {error_type} - {reason}")
            stop_event.set()

    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")

def on_error(ws, error):
"""Called when a WebSocket error occurs."""
print(f"\nWebSocket Error: {error}") # Attempt to signal stop on error
stop_event.set()

def on_close(ws, close_status_code, close_msg):
"""Called when the WebSocket connection is closed."""
print(f"\nWebSocket Disconnected: Status={close_status_code}, Msg={close_msg}") # Ensure audio resources are released
global stream, audio
stop_event.set() # Signal audio thread just in case it's still running

    if stream:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        stream = None
    if audio:
        audio.terminate()
        audio = None
    # Try to join the audio thread to ensure clean exit
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=1.0)

# --- Main Execution ---

def run():
global audio, stream, ws_app, SAMPLE_RATE

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Get default input device (can alter to specify specific device)
    default_device = audio.get_default_input_device_info()
    device_index = default_device['index']
    SAMPLE_RATE = int(audio.get_device_info_by_index(device_index)['defaultSampleRate'])

    print(f"Using microphone: {default_device['name']}")

    # Open microphone stream
    try:
        stream = audio.open(
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            channels=CHANNELS,
            format=FORMAT,
            rate=SAMPLE_RATE,
            input_device_index=device_index
        )
        print("Microphone stream opened successfully.")
        print("Speak into your microphone. Press Ctrl+C to stop.")
    except Exception as e:
        print(f"Error opening microphone stream: {e}")
        if audio:
            audio.terminate()
        return  # Exit if microphone cannot be opened

    # Create WebSocketApp
    ws_app = websocket.WebSocketApp(
        API_ENDPOINT,
        header={"Authorization": f"Bearer {YOUR_API_KEY}"},  # Speechmatics uses Bearer token
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Run WebSocketApp in a separate thread to allow main thread to catch KeyboardInterrupt
    ws_thread = threading.Thread(target=lambda: ws_app.run_forever(ping_interval=30, ping_timeout=10))
    ws_thread.daemon = True
    ws_thread.start()

    try:
        # Keep main thread alive until interrupted
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nCtrl+C received. Stopping...")
        stop_event.set()  # Signal audio thread to stop

        # Send EndOfStream message to the server
        if ws_app and ws_app.sock and ws_app.sock.connected:
            try:
                end_message = {
                    "message": "EndOfStream",
                    "last_seq_no": audio_seq_no
                }
                print(f"Sending termination message: {json.dumps(end_message)}")
                ws_app.send(json.dumps(end_message))
                # Give a moment for messages to process before forceful close
                time.sleep(1)
            except Exception as e:
                print(f"Error sending termination message: {e}")

        # Close the WebSocket connection (will trigger on_close)
        if ws_app:
            ws_app.close()

        # Wait for WebSocket thread to finish
        ws_thread.join(timeout=2.0)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        stop_event.set()
        if ws_app:
            ws_app.close()
        ws_thread.join(timeout=2.0)

    finally:
        # Final cleanup (already handled in on_close, but good as a fallback)
        if stream and stream.is_active():
            stream.stop_stream()
        if stream:
            stream.close()
        if audio:
            audio.terminate()
        print("Cleanup complete. Exiting.")

if **name** == "**main**":
run()

````
</Tab>

<Tab language="aai" title="AssemblyAI">
```python
import pyaudio
import websocket
import json
import threading
import time
from urllib.parse import urlencode
from datetime import datetime

# --- Configuration ---
YOUR_API_KEY = "YOUR-API-KEY"  # Replace with your actual API key

CONNECTION_PARAMS = {
    "sample_rate": 16000,
    "format_turns": True,  # Request formatted final transcripts
}
API_ENDPOINT_BASE_URL = "wss://streaming.assemblyai.com/v3/ws"
API_ENDPOINT = f"{API_ENDPOINT_BASE_URL}?{urlencode(CONNECTION_PARAMS)}"

# Audio Configuration
FRAMES_PER_BUFFER = 800  # 50ms of audio (0.05s * 16000Hz)
SAMPLE_RATE = CONNECTION_PARAMS["sample_rate"]
CHANNELS = 1
FORMAT = pyaudio.paInt16

# Global variables for audio stream and websocket
audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event()  # To signal the audio thread to stop

# --- WebSocket Event Handlers ---
def on_open(ws):
    """Called when the WebSocket connection is established."""
    print("WebSocket connection opened.")
    print(f"Connected to: {API_ENDPOINT}")

    # Start sending audio data in a separate thread
    def stream_audio():
        global stream
        print("Starting audio streaming...")
        while not stop_event.is_set():
            try:
                audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                # Send audio data as binary message
                ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
            except Exception as e:
                print(f"Error streaming audio: {e}")
                # If stream read fails, likely means it's closed, stop the loop
                break
        print("Audio streaming stopped.")

    global audio_thread
    audio_thread = threading.Thread(target=stream_audio)
    audio_thread.daemon = (
        True  # Allow main thread to exit even if this thread is running
    )
    audio_thread.start()

def on_message(ws, message):
    try:
        data = json.loads(message)
        msg_type = data.get('type')

        if msg_type == "Begin":
            session_id = data.get('id')
            expires_at = data.get('expires_at')
            print(f"\nSession began: ID={session_id}, ExpiresAt={datetime.fromtimestamp(expires_at)}")
        elif msg_type == "Turn":
            transcript = data.get('transcript', '')
            formatted = data.get('turn_is_formatted', False)

            # Clear previous line for formatted messages
            if formatted:
                print('\r' + ' ' * 80 + '\r', end='')
                print(transcript)
            else:
                print(f"\r{transcript}", end='')
        elif msg_type == "Termination":
            audio_duration = data.get('audio_duration_seconds', 0)
            session_duration = data.get('session_duration_seconds', 0)
            print(f"\nSession Terminated: Audio Duration={audio_duration}s, Session Duration={session_duration}s")
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")

def on_error(ws, error):
    """Called when a WebSocket error occurs."""
    print(f"\nWebSocket Error: {error}")
    # Attempt to signal stop on error
    stop_event.set()

def on_close(ws, close_status_code, close_msg):
    """Called when the WebSocket connection is closed."""
    print(f"\nWebSocket Disconnected: Status={close_status_code}, Msg={close_msg}")
    # Ensure audio resources are released
    global stream, audio
    stop_event.set()  # Signal audio thread just in case it's still running

    if stream:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        stream = None
    if audio:
        audio.terminate()
        audio = None
    # Try to join the audio thread to ensure clean exit
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=1.0)

# --- Main Execution ---
def run():
    global audio, stream, ws_app

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open microphone stream
    try:
        stream = audio.open(
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            channels=CHANNELS,
            format=FORMAT,
            rate=SAMPLE_RATE,
        )
        print("Microphone stream opened successfully.")
        print("Speak into your microphone. Press Ctrl+C to stop.")
    except Exception as e:
        print(f"Error opening microphone stream: {e}")
        if audio:
            audio.terminate()
        return  # Exit if microphone cannot be opened

    # Create WebSocketApp
    ws_app = websocket.WebSocketApp(
        API_ENDPOINT,
        header={"Authorization": YOUR_API_KEY},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Run WebSocketApp in a separate thread to allow main thread to catch KeyboardInterrupt
    ws_thread = threading.Thread(target=ws_app.run_forever)
    ws_thread.daemon = True
    ws_thread.start()

    try:
        # Keep main thread alive until interrupted
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nCtrl+C received. Stopping...")
        stop_event.set()  # Signal audio thread to stop

        # Send termination message to the server
        if ws_app and ws_app.sock and ws_app.sock.connected:
            try:
                terminate_message = {"type": "Terminate"}
                print(f"Sending termination message: {json.dumps(terminate_message)}")
                ws_app.send(json.dumps(terminate_message))
                # Give a moment for messages to process before forceful close
                time.sleep(5)
            except Exception as e:
                print(f"Error sending termination message: {e}")

        # Close the WebSocket connection (will trigger on_close)
        if ws_app:
            ws_app.close()

        # Wait for WebSocket thread to finish
        ws_thread.join(timeout=2.0)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        stop_event.set()
        if ws_app:
            ws_app.close()
        ws_thread.join(timeout=2.0)

    finally:
        # Final cleanup (already handled in on_close, but good as a fallback)
        if stream and stream.is_active():
            stream.stop_stream()
        if stream:
            stream.close()
        if audio:
            audio.terminate()
        print("Cleanup complete. Exiting.")

if __name__ == "__main__":
    run()
````

</Tab>
</Tabs>

## Step 1: Install dependencies

<Steps>
<Step>

<Tabs groupId="language">
<Tab language="speechmatics" title="Speechmatics">

Install the required Python packages.

```bash
pip install websocket-client pyaudio
