import logging
from typing import Type
import threading
import time
import wave
import numpy as np
import pyaudio

import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent,
)

# Configuration
API_KEY = "<YOUR_API_KEY>"
AUDIO_FILE_PATH = "<DUAL_CHANNEL_AUDIO_FILE_PATH>"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChannelTranscriber:
    def __init__(self, channel_id, channel_name, sample_rate):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.sample_rate = sample_rate
        self.client = None
        self.audio_data = []
        self.current_turn_line = None
        self.line_count = 0
        self.streaming_done = threading.Event()

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

    def clear_current_line(self):
        if self.current_turn_line is not None:
            print("\r" + " " * 100 + "\r", end="", flush=True)

    def print_partial_transcript(self, words):
        self.clear_current_line()
        # Build transcript from individual words
        word_texts = [word.text for word in words]
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

    def on_begin(self, client: Type[StreamingClient], event: BeginEvent):
        """Called when the streaming session begins."""
        pass  # Session started

    def on_turn(self, client: Type[StreamingClient], event: TurnEvent):
        """Called when a turn is received."""
        transcript = event.transcript.strip() if event.transcript else ''
        formatted = event.turn_is_formatted
        words = event.words if event.words else []

        if transcript or words:
            if formatted:
                self.print_final_transcript(transcript)
            else:
                self.print_partial_transcript(words)

    def on_terminated(self, client: Type[StreamingClient], event: TerminationEvent):
        """Called when the session is terminated."""
        self.clear_current_line()
        self.streaming_done.set()

    def on_error(self, client: Type[StreamingClient], error: StreamingError):
        """Called when an error occurs."""
        print(f"\n{self.channel_name}: Error: {error}")
        self.streaming_done.set()

    def start_transcription(self):
        """Start the transcription for this channel."""
        self.load_audio_channel()

        # Create streaming client
        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=API_KEY,
                api_host="streaming.assemblyai.com",
            )
        )

        # Register event handlers
        self.client.on(StreamingEvents.Begin, self.on_begin)
        self.client.on(StreamingEvents.Turn, self.on_turn)
        self.client.on(StreamingEvents.Termination, self.on_terminated)
        self.client.on(StreamingEvents.Error, self.on_error)

        # Connect to streaming service with turn detection configuration
        self.client.connect(
            StreamingParameters(
                sample_rate=self.sample_rate,
                format_turns=True,
                end_of_turn_confidence_threshold=0.4,
                min_end_of_turn_silence_when_confident=160,
                max_turn_silence=400,
            )
        )

        # Create audio generator
        def audio_generator():
            for chunk in self.audio_data:
                yield chunk
                time.sleep(0.05)  # 50ms intervals

        try:
            # Stream audio
            self.client.stream(audio_generator())
        finally:
            # Disconnect
            self.client.disconnect(terminate=True)
            self.streaming_done.set()

    def start_transcription_thread(self):
        """Start transcription in a separate thread."""
        thread = threading.Thread(target=self.start_transcription, daemon=True)
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
    # Get sample rate from file
    with wave.open(AUDIO_FILE_PATH, 'rb') as wf:
        sample_rate = wf.getframerate()

    # Create transcribers for each channel
    transcriber_1 = ChannelTranscriber(0, "Speaker 1", sample_rate)
    transcriber_2 = ChannelTranscriber(1, "Speaker 2", sample_rate)

    # Start audio playback
    audio_thread = threading.Thread(target=play_audio_file, daemon=True)
    audio_thread.start()

    # Start both transcriptions
    thread_1 = transcriber_1.start_transcription_thread()
    thread_2 = transcriber_2.start_transcription_thread()

    # Wait for completion
    thread_1.join()
    thread_2.join()
    audio_thread.join()


if __name__ == "__main__":
    transcribe_multichannel()