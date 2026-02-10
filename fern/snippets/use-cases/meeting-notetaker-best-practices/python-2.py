# pip install pyaudio websocket-client
import pyaudio
import websocket
import json
import threading
import time
from urllib.parse import urlencode
from datetime import datetime

# --- Configuration ---
YOUR_API_KEY = "your_api_key"

# Keyterms to improve recognition accuracy
KEYTERMS = [
    "Alice Johnson",
    "Bob Smith",
    "Carol Davis",
    "quarterly review",
    "action items",
    "follow up",
    "deadline",
    "budget"
]

# MEETING NOTETAKER CONFIGURATION (different from voice agents!)
CONNECTION_PARAMS = {
    "sample_rate": 16000,
    "format_turns": True,  # ALWAYS TRUE for meetings - users need readable text

    # Meeting-optimized turn detection (wait longer than voice agents)
    "end_of_turn_confidence_threshold": 0.6,  # Higher than voice agents (0.4)
    "min_end_of_turn_silence_when_confident": 560,  # Wait longer for natural pauses (voice agents use 160ms)
    "max_turn_silence": 2000,  # Allow thinking pauses (voice agents use 1280ms)

    # Keyterms for accuracy
    "keyterms_prompt": json.dumps(KEYTERMS)
}

API_ENDPOINT_BASE_URL = "wss://streaming.assemblyai.com/v3/ws"
API_ENDPOINT = f"{API_ENDPOINT_BASE_URL}?{urlencode(CONNECTION_PARAMS)}"

# Audio Configuration
FRAMES_PER_BUFFER = 800  # 50ms of audio
SAMPLE_RATE = CONNECTION_PARAMS["sample_rate"]
CHANNELS = 1
FORMAT = pyaudio.paInt16

# Global variables
audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event()
transcript_buffer = []


def on_open(ws):
    """Called when the WebSocket connection is established."""
    print("=" * 80)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Meeting transcription started")
    print(f"Connected to: {API_ENDPOINT_BASE_URL}")
    print(f"Keyterms configured: {', '.join(KEYTERMS)}")
    print("=" * 80)
    print("\nSpeak into your microphone. Press Ctrl+C to stop.\n")

    def stream_audio():
        """Stream audio from microphone to WebSocket"""
        global stream
        while not stop_event.is_set():
            try:
                audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)
            except Exception as e:
                if not stop_event.is_set():
                    print(f"Error streaming audio: {e}")
                break

    global audio_thread
    audio_thread = threading.Thread(target=stream_audio)
    audio_thread.daemon = True
    audio_thread.start()


def on_message(ws, message):
    """Handle incoming messages from AssemblyAI"""
    try:
        data = json.loads(message)
        msg_type = data.get("type")

        # Uncomment to see full JSON for debugging:
        # print("=" * 80)
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        # print("=" * 80)
        # print()

        if msg_type == "Begin":
            session_id = data.get("id", "N/A")
            print(f"[SESSION] Started - ID: {session_id}\n")

        elif msg_type == "Turn":
            end_of_turn = data.get("end_of_turn", False)
            turn_is_formatted = data.get("turn_is_formatted", False)
            transcript = data.get("transcript", "")
            turn_order = data.get("turn_order", 0)
            end_of_turn_confidence = data.get("end_of_turn_confidence", 0.0)

            # FOR MEETING NOTETAKERS: Show partials for responsive UI
            if not end_of_turn and transcript:
                print(f"\r[LIVE] {transcript}", end="", flush=True)

            # FOR MEETING NOTETAKERS: Use formatted finals for readable display
            # (Unlike voice agents which should use utterance for speed)
            if end_of_turn and turn_is_formatted and transcript:
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"\n[{timestamp}] {transcript}")
                print(f"           Turn: {turn_order} | Confidence: {end_of_turn_confidence:.2%}")

                # Detect action items
                transcript_lower = transcript.lower()
                if any(term in transcript_lower for term in ["action item", "follow up", "deadline", "assigned to", "todo"]):
                    print("           ⚠️  ACTION ITEM DETECTED!")

                # Store final transcript
                transcript_buffer.append({
                    "timestamp": timestamp,
                    "text": transcript,
                    "turn_order": turn_order,
                    "confidence": end_of_turn_confidence,
                    "type": "final"
                })
                print()

        elif msg_type == "Termination":
            audio_duration = data.get("audio_duration_seconds", 0)
            print(f"\n[SESSION] Terminated - Duration: {audio_duration}s")
            save_transcript()

        elif msg_type == "Error":
            error_msg = data.get("error", "Unknown error")
            print(f"\n[ERROR] {error_msg}")

    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")


def on_error(ws, error):
    """Called when a WebSocket error occurs."""
    print(f"\n[WEBSOCKET ERROR] {error}")
    stop_event.set()


def on_close(ws, close_status_code, close_msg):
    """Called when the WebSocket connection is closed."""
    print(f"\n[WEBSOCKET] Disconnected - Status: {close_status_code}, Message: {close_msg}")

    global stream, audio
    stop_event.set()

    # Clean up audio stream
    if stream:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        stream = None
    if audio:
        audio.terminate()
        audio = None
    if audio_thread and audio_thread.is_alive():
        audio_thread.join(timeout=1.0)


def save_transcript():
    """Save the transcript to a file"""
    if not transcript_buffer:
        print("No transcript to save.")
        return

    filename = f"meeting_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("Meeting Transcript\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Keyterms: {', '.join(KEYTERMS)}\n")
        f.write("=" * 80 + "\n\n")

        for entry in transcript_buffer:
            f.write(f"[{entry['timestamp']}] {entry['text']}\n")
            f.write(f"Confidence: {entry['confidence']:.2%}\n\n")

    print(f"Transcript saved to: {filename}")


def run():
    """Main function to run the streaming transcription"""
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
    except Exception as e:
        print(f"Error opening microphone stream: {e}")
        if audio:
            audio.terminate()
        return

    # Create WebSocketApp
    ws_app = websocket.WebSocketApp(
        API_ENDPOINT,
        header={"Authorization": YOUR_API_KEY},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Run WebSocketApp in a separate thread
    ws_thread = threading.Thread(target=ws_app.run_forever)
    ws_thread.daemon = True
    ws_thread.start()

    try:
        # Keep main thread alive until interrupted
        while ws_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nCtrl+C received. Stopping transcription...")
        stop_event.set()

        # Send termination message to the server
        if ws_app and ws_app.sock and ws_app.sock.connected:
            try:
                terminate_message = {"type": "Terminate"}
                ws_app.send(json.dumps(terminate_message))
                time.sleep(1)
            except Exception as e:
                print(f"Error sending termination message: {e}")

        if ws_app:
            ws_app.close()

        ws_thread.join(timeout=2.0)

    finally:
        # Final cleanup
        if stream and stream.is_active():
            stream.stop_stream()
        if stream:
            stream.close()
        if audio:
            audio.terminate()
        print("Cleanup complete. Exiting.")


if __name__ == "__main__":
    run()
