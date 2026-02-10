import pyaudio

CONNECTION_PARAMS = {
"sample_rate": 16000,
"format_turns": True, # Request formatted final transcripts
}

# Audio Configuration

FRAMES_PER_BUFFER = 800 # 50ms of audio (0.05s \* 16000Hz)
SAMPLE_RATE = CONNECTION_PARAMS["sample_rate"]
CHANNELS = 1
FORMAT = pyaudio.paInt16

# Global variables for audio stream and websocket

audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event() # To signal the audio thread to stop

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

````
<Tip title="Sample rate">
Using a sample rate of `16 kHz` and encoding of `pcm_s16le` is recommended, as our STT model operates at a `16 kHz` sample rate.
If the incoming audio uses a different rate, we perform additional sampling rate conversion under the hood, which might marginally increase latency.
</Tip>
</Tab>
</Tabs>

<Note title="Audio data format">

If you want to stream data from elsewhere, make sure that your audio data is in the following format:

- Single-channel
- PCM16 (default) or Mu-law encoding (see [Specifying the encoding](/docs/speech-to-text/streaming#specify-the-encoding))
- A sample rate that matches the value of the `sample_rate` parameter (16 kHz is recommended)
- 50 milliseconds of audio per message (larger chunk sizes are workable, but may result in latency fluctuations)

</Note>

</Step>
</Steps>

## Step 4: Create event handlers

In this step, you’ll set up callback functions that handle the different events.

<Steps>
<Step>

Create functions to handle the events from the real-time service.

<Tabs groupId="language">
<Tab language="speechmatics" title="Speechmatics">
```python
import json

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
````

</Tab>

<Tab language="aai" title="AssemblyAI">
```python
import threading

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

````

</Tab>
</Tabs>

<Note title="Connection configuration">
**Speechmatics** requires a **handshake** where the connection configuration is specified before audio is streamed. **AssemblyAI** allows you to configure the connection via query parameters in the URL and start streaming audio immediately.

The **Speechmatics** handshake begins when `on_open` sends a `StartRecognition` message to configure the session. Audio streaming only starts after the `RecognitionStarted` message type is parsed and confirmed in the `on_message` callback.
</Note>

</Step>
<Step>

Create another function to handle transcripts.

**Speechmatics** has separate partial (`AddPartialTranscript`) and final (`AddTranscript`) transcripts. The terminate session message is `EndOfTranscript`.

**AssemblyAI** instead uses a `Turn` object with a `turn_is_formatted` boolean flag to indicate finality. The terminate session message is `Termination`.
For more on the Turn object, see **Streaming** [Core concepts](/docs/speech-to-text/universal-streaming#core-concepts) section.

<Tabs groupId="language">
<Tab language="speechmatics" title="Speechmatics">
```python
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
````

</Tab>
<Tab language="aai" title="AssemblyAI">
```python
import json
from datetime import datetime

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

````
</Tab>
</Tabs>
</Step>

<Note title="Transcript message structure">
  Please note the difference in transcript message structure below:
  ```python
  # Speechmatics
  {
    "message": "AddPartialTranscript",
    "metadata": {
      "transcript": "hello world"
    },
    # Other transcript data...
  }

  # AssemblyAI
  {
    "type": "Turn",
    "transcript": "hello world",
    "turn_is_formatted": false,
    # Other transcript data...
  }
````

</Note>
</Steps>

## Step 5: Connect and start transcription

<Steps>
<Step>
To stream audio, establish a connection to the API via [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API).

<Tabs groupId="language">
<Tab language="speechmatics" title="Speechmatics">
Create a WebSocket connection to the Realtime service.
```python
def run():
    global audio, stream, ws_app, SAMPLE_RATE
    # Skipping audio/microphone setup code...

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

````

</Tab>
<Tab language="aai" title="AssemblyAI">

Create and run a WebSocket connection to the Realtime service.

```python
import websocket
import threading

def run():
    global audio, stream, ws_app
    # Skipping audio/microphone setup code...

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
````

</Tab>
</Tabs>

<Note title="Authorization ">
  Note that while both services use an `Authorization` header to authenticate
  the WebSocket connection, **Speechmatics** uses a `Bearer` prefix, while
  **AssemblyAI** does not.
</Note>

</Step>
</Steps>

## Step 6: Close the connection

<Steps>
<Step>

Keep the main thread alive until interrupted, handle keyboard interrupts and thrown exceptions, and clean up upon closing of the WebSocket connection.

<Tabs groupId="language">
<Tab language="speechmatics" title="Speechmatics">

```python
def run():
    global audio, stream, ws_app, SAMPLE_RATE
    # Skipping audio/microphone setup and WebSocket connection code...

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
