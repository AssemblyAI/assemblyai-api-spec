import websocket
import json
import threading
import numpy as np
import wave
import time
import pyaudio
from urllib.parse import urlencode

# Configuration
YOUR_API_KEY = "<YOUR_API_KEY>"
AUDIO_FILE_PATH = "<DUAL_CHANNEL_AUDIO_FILE_PATH>"
API_BASE_URL = "wss://streaming.assemblyai.com/v3/ws"
API_PARAMS = {
    "sample_rate": 8000,
    "format_turns": "true",
    "end_of_turn_confidence_threshold": 0.4,
    "min_end_of_turn_silence_when_confident": 160,
    "max_turn_silence": 400,
}
# Build API endpoint with URL encoding
API_ENDPOINT = f"{API_BASE_URL}?{urlencode(API_PARAMS)}"

class ChannelTranscriber:
    def __init__(self, channel_id, channel_name):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.ws_app = None
        self.audio_data = []
        self.current_turn_line = None
        self.line_count = 0

    def load_audio_channel(self):
        """Extract single channel from dual-channel audio file."""
        with wave.open(AUDIO_FILE_PATH, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            audio_array = np.frombuffer(frames, dtype=np.int16)

            if wf.getnchannels() == 2:
                audio_array = audio_array.reshape(-1, 2)
                channel_audio = audio_array[:, self.channel_id]

                # Split into chunks for streaming
                FRAMES_PER_BUFFER = 400  # 50ms chunks
                for i in range(0, len(channel_audio), FRAMES_PER_BUFFER):
                    chunk = channel_audio[i:i+FRAMES_PER_BUFFER]
                    if len(chunk) < FRAMES_PER_BUFFER:
                        chunk = np.pad(chunk, (0, FRAMES_PER_BUFFER - len(chunk)), 'constant')
                    self.audio_data.append(chunk.astype(np.int16).tobytes())

    def on_open(self, ws):
        """Stream audio data when connection opens."""
        def stream_audio():
            for chunk in self.audio_data:
                ws.send(chunk, websocket.ABNF.OPCODE_BINARY)
                time.sleep(0.05)  # 50ms intervals

            # Send termination message
            terminate_message = {"type": "Terminate"}
            ws.send(json.dumps(terminate_message))

        threading.Thread(target=stream_audio, daemon=True).start()

    def clear_current_line(self):
        if self.current_turn_line is not None:
            print("\r" + " " * 100 + "\r", end="", flush=True)

    def print_partial_transcript(self, words):
        self.clear_current_line()
        # Build transcript from individual words
        word_texts = [word.get('text', '') for word in words]
        transcript = ' '.join(word_texts)
        partial_text = f"{self.channel_name}: {transcript}"
        print(partial_text, end="", flush=True)
        self.current_turn_line = len(partial_text)

    def print_final_transcript(self, transcript):
        self.clear_current_line()
        final_text = f"{self.channel_name}: {transcript}"
        print(final_text, flush=True)
        self.current_turn_line = None
        self.line_count += 1

    def on_message(self, ws, message):
        """Handle transcription results."""
        data = json.loads(message)
        msg_type = data.get('type')

        if msg_type == "Turn":
            transcript = data.get('transcript', '').strip()
            formatted = data.get('turn_is_formatted', False)
            words = data.get('words', [])

            if transcript or words:
                if formatted:
                    self.print_final_transcript(transcript)
                else:
                    self.print_partial_transcript(words)

    def start_transcription(self):
        self.load_audio_channel()

        self.ws_app = websocket.WebSocketApp(
            API_ENDPOINT,
            header={"Authorization": YOUR_API_KEY},
            on_open=self.on_open,
            on_message=self.on_message,
        )

        thread = threading.Thread(target=self.ws_app.run_forever, daemon=True)
        thread.start()
        return thread

def play_audio_file():
    try:
        with wave.open(AUDIO_FILE_PATH, 'rb') as wf:
            p = pyaudio.PyAudio()

            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            print(f"Playing audio: {AUDIO_FILE_PATH}")

            # Play audio in chunks
            chunk_size = 1024
            data = wf.readframes(chunk_size)

            while data:
                stream.write(data)
                data = wf.readframes(chunk_size)

            stream.stop_stream()
            stream.close()
            p.terminate()

            print("Audio playback finished")

    except Exception as e:
        print(f"Error playing audio: {e}")


def transcribe_multichannel():
    # Create transcribers for each channel
    transcriber_1 = ChannelTranscriber(0, "Speaker 1")
    transcriber_2 = ChannelTranscriber(1, "Speaker 2")

    # Start audio playback
    audio_thread = threading.Thread(target=play_audio_file, daemon=True)
    audio_thread.start()

    # Start both transcriptions
    thread_1 = transcriber_1.start_transcription()
    thread_2 = transcriber_2.start_transcription()

    # Wait for completion
    thread_1.join()
    thread_2.join()
    audio_thread.join()

if __name__ == "__main__":
    transcribe_multichannel()
