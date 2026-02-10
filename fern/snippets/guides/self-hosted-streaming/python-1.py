"""
Example script for streaming audio to AssemblyAI's self-hosted streaming transcription API.
This is a minimal reference implementation for demonstration purposes only.
For production use cases, best practices, and the complete API specification, please visit https://www.assemblyai.com/docs
"""

import argparse
import json
import logging
import math
import os
import time
import wave
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from urllib.parse import urlencode

from websockets.sync.client import ClientConnection, connect

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class AudioChunk:
    data: bytes
    duration_ms: int


def _validate_and_get_pcm16_raw_bytes(
    wav_file_path: str, expected_sample_rate: int
) -> bytes:
    """
    Validate that the WAV file is PCM16 encoded with the expected sample rate and extract raw audio data.

    :param wav_file_path: Path to the WAV file.
    :param expected_sample_rate: Expected sample rate (e.g., 16000).
    :return: Raw audio content as bytes.
    :raises ValueError: If the file is not PCM16 or doesn't match expected sample rate.
    """
    with wave.open(wav_file_path, "rb") as wav_file:
        # Check if it's PCM16
        if wav_file.getsampwidth() != 2:
            raise ValueError(
                f"Audio file must be 16-bit PCM. Found sample width: {wav_file.getsampwidth() * 8}-bit"
            )

        if wav_file.getcomptype() != "NONE":
            raise ValueError(
                f"Audio file must be uncompressed PCM. Found compression type: {wav_file.getcomptype()}"
            )

        # Check sample rate
        actual_sample_rate = wav_file.getframerate()
        if actual_sample_rate != expected_sample_rate:
            raise ValueError(
                f"Audio file must have sample rate of {expected_sample_rate} Hz. "
                f"Found: {actual_sample_rate} Hz"
            )

        # Check if mono
        if wav_file.getnchannels() != 1:
            raise ValueError(
                f"Audio file must be mono (1 channel). Found: {wav_file.getnchannels()} channels"
            )

        raw_audio = wav_file.readframes(wav_file.getnframes())

    return raw_audio


def _get_chunks_from_file(
    filepath: str,
    sample_rate: int,
    chunk_size_ms: int,
) -> List[AudioChunk]:
    """
    Read a PCM16 WAV file and split it into chunks.

    :param filepath: Path to the PCM16 WAV file.
    :param sample_rate: Expected sample rate of the audio file.
    :param chunk_size_ms: Duration of each chunk in milliseconds.
    :return: List of AudioChunk objects.
    :raises ValueError: If the file is not in the correct format.
    """
    chunks = []
    audio_bytes: bytes = _validate_and_get_pcm16_raw_bytes(filepath, sample_rate)

    read_bytes = 0
    while read_bytes < len(audio_bytes):
        frame_size = 2  # 16-bit PCM (2 bytes per sample)
        chunk_bytes_len = int(sample_rate * chunk_size_ms * frame_size // 1000)
        data = audio_bytes[read_bytes : read_bytes + chunk_bytes_len]
        read_bytes += len(data)
        actual_chunk_ms = math.ceil(len(data) * 1000 / (sample_rate * frame_size))
        chunks.append(AudioChunk(data=data, duration_ms=actual_chunk_ms))

    return chunks


def _write_to_ws(ws: ClientConnection, audio_chunks: List[AudioChunk]) -> None:
    """
    Write audio chunks to the WebSocket connection.

    :param ws: WebSocket connection.
    :param audio_chunks: List of audio chunks to send.
    """
    try:
        for chunk in audio_chunks:
            # Sleep for the chunk duration to send chunks with realtime rate
            time.sleep(chunk.duration_ms / 1000)
            ws.send(chunk.data)
        ws.send('{"type": "Terminate"}')
    except Exception as e:
        LOGGER.error(
            f"Exception occurred while writing to websocket: {e}", exc_info=True
        )
        ws.close()
        raise


def _read_from_ws(ws: ClientConnection) -> None:
    """
    Read and process messages from the WebSocket connection.

    :param ws: WebSocket connection.
    """
    try:
        for message in ws:
            data = json.loads(message)
            if "type" not in data:
                raise Exception(f"Unknown message received: {data}")
            elif data["type"] == "Turn":
                if data["words"]:
                    text = " ".join([word["text"] for word in data["words"]])
                    audio_start = data["words"][0]["start"]
                    audio_end = data["words"][-1]["end"]
                    end_of_turn = "True " if data["end_of_turn"] else "False"
                    LOGGER.info(
                        f"{timedelta(milliseconds=audio_start)}-"
                        f"{timedelta(milliseconds=audio_end)}, end-of-turn: {end_of_turn}: {text}",
                    )
            elif data["type"] == "Begin":
                expires_at = datetime.fromtimestamp(int(data["expires_at"]))
                LOGGER.info(
                    f"Session started. Session id: {data['id']}, expires at: {expires_at}",
                )
            elif data["type"] == "Termination":
                LOGGER.info(
                    f"Session completed with session duration: {data['session_duration_seconds']} sec.",
                )
            else:
                LOGGER.error(f"Unknown message type: {data}")
    except Exception as e:
        LOGGER.error(
            f"Exception occurred while reading from the websocket: {e}", exc_info=True
        )
        ws.close()
        raise


def run_session(
    api_endpoint: str,
    audio_chunks: List[AudioChunk],
    sample_rate: int,
    keyterms_prompt: Optional[List[str]] = None,
    language: Optional[str] = None,
) -> None:
    """
    Run a WebSocket session to stream audio and receive transcriptions.

    :param api_endpoint: WebSocket endpoint URL.
    :param audio_chunks: List of audio chunks to send.
    :param sample_rate: Sample rate of the audio.
    :param keyterms_prompt: Optional list of key terms for the transcription.
    :param language: Optional language code for transcription.
    """
    try:
        params = {
            "sample_rate": sample_rate,
        }
        if keyterms_prompt:
            params["keyterms"] = json.dumps(keyterms_prompt)
        if language:
            params["language"] = language

        endpoint_str = f"{api_endpoint}?{urlencode(params)}"
        headers = {"Authorization": "self-hosted"}
        LOGGER.info(f"Endpoint: {endpoint_str}")
        with ThreadPoolExecutor(max_workers=2) as executor:
            with connect(endpoint_str, additional_headers=headers) as websocket:
                write_future = executor.submit(
                    _write_to_ws,
                    websocket,
                    audio_chunks,
                )
                read_future = executor.submit(
                    _read_from_ws,
                    websocket,
                )
                write_future.result()
                read_future.result()
    except Exception as e:
        LOGGER.error(
            f"Exception occurred: {e}",
            exc_info=True,
        )
        raise


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Stream audio to AssemblyAI self-hosted real-time transcription service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default endpoint
  python example_with_prerecorded_audio_file.py --audio-file example_audio_file.wav

  # Specify custom endpoint and language
  python example_with_prerecorded_audio_file.py --audio-file example_audio_file.wav --endpoint ws://localhost:8080 --language multi

Note: Audio file must be PCM 16-bit WAV format, mono channel, 16kHz sample rate.
        """,
    )
    parser.add_argument(
        "--audio-file",
        type=str,
        default=os.path.dirname(__file__) + os.path.sep + "example_audio_file.wav",
        help="Path to the audio file to transcribe (must be PCM 16-bit WAV, mono, 16kHz)",
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        default="ws://localhost:8080",
        help="WebSocket endpoint URL (default: ws://localhost:8080)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="",
        help="Language code for transcription (e.g., 'multi')",
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_args()
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        sample_rate = 16_000

        audio_chunks = _get_chunks_from_file(
            args.audio_file,
            sample_rate=sample_rate,
            chunk_size_ms=100,
        )
        run_session(
            api_endpoint=args.endpoint,
            audio_chunks=audio_chunks,
            sample_rate=sample_rate,
            language=args.language if args.language else None,
        )
    except KeyboardInterrupt:
        LOGGER.info("Interrupted by user, exiting.")
        exit(0)
    except ValueError as e:
        LOGGER.error(f"Audio file validation error: {e}")
        exit(1)
