# pip install assemblyai whisper-normalizer jiwer
import jiwer
from whisper_normalizer.english import EnglishTextNormalizer
from whisper_normalizer.basic import BasicTextNormalizer

import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent
)
from typing import Type

# Global variable to collect assembly transcripts
assembly_streaming_transcript = ""

def on_begin(self: Type[StreamingClient], event: BeginEvent):
  "This function is called when the connection has been established."

  print("Session ID:", event.id)

def on_turn(self: Type[StreamingClient], event: TurnEvent):
  "This function is called when a new transcript has been received."
  global assembly_streaming_transcript

  if event.end_of_turn and event.turn_is_formatted:
    assembly_streaming_transcript += event.transcript + " "

  print(event.transcript, end="\r\n")

def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
  "This function is called when an error occurs."

  print(
    f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
  )

def on_error(self: Type[StreamingClient], error: StreamingError):
  "This function is called when the connection has been closed."

  print(f"Error occurred: {error}")


# Create the streaming client
client = StreamingClient(
  StreamingClientOptions(
    api_key="YOUR-API-KEY"
  )
)

client.on(StreamingEvents.Begin, on_begin)
client.on(StreamingEvents.Turn, on_turn)
client.on(StreamingEvents.Termination, on_terminated)
client.on(StreamingEvents.Error, on_error)

def stream_file(filepath: str, sample_rate: int):
    """Stream audio file in 50ms chunks instead of 300ms"""
    import time
    import wave

    chunk_duration = 0.1

    with wave.open(filepath, 'rb') as wav_file:
        if wav_file.getnchannels() != 1:
            raise ValueError("Only mono audio is supported")

        file_sample_rate = wav_file.getframerate()
        if file_sample_rate != sample_rate:
            print(f"Warning: File sample rate ({file_sample_rate}) doesn't match expected rate ({sample_rate})")

        frames_per_chunk = int(file_sample_rate * chunk_duration)

        while True:
            frames = wav_file.readframes(frames_per_chunk)

            if not frames:
                break

            yield frames

            # time.sleep(chunk_duration)

file_stream = stream_file(
  filepath="audio.wav",
  sample_rate=48000,
)

client.connect(
    StreamingParameters(
        sample_rate=48000,
        format_turns=True,
    )
)

try:
    client.stream(file_stream)
finally:
    client.disconnect(terminate=True)

# Evaluate collected transcripts
reference_transcript = "AssemblyAI is a deep learning company that builds powerful APIs to help you transcribe and understand audio. The most common use case for the API is to automatically convert prerecorded audio and video files as well as real time audio streams into text transcriptions. Our APIs convert audio and video into text using powerful deep learning models that we research and develop end to end in house. Millions of podcasts, zoom recordings, phone calls or video files are being transcribed with Assembly AI every single day. But where Assembly AI really excels is with helping you understand your data. So let's say we transcribe Joe Biden's State of the Union using Assembly AI's API. With our Auto Chapters feature, you can generate time coded summaries of the key moments of your audio file. For example, with the State of the Union address we get chapter summaries like this. Auto Chapters automatically segments your audio or video files into chapters and provides a summary for each of these chapters. With Sentiment Analysis, we can classify what's being spoken in your audio files as either positive, negative or neutral. So for example, in the State of the Union address we see that this sentence was classified as positive, whereas this sentence was classified as negative. Content Safety Detection can flag sensitive content as it is spoken like hate speech, profanity, violence or weapons. For example, in Biden's State of the Union address, content safety detection flagged parts of his speech as being about weapons. This feature is especially useful for automatic content moderation and brand safety use cases. With Auto Highlights, you can automatically identify important words and phrases that are being spoken in your data owned by the State of the Union address. AssemblyAI's API detected these words and phrases as being important. Lastly, with entity detection you can identify entities that are spoken in your audio like organization names or person names. In Biden's speech, these were the entities that were detected. This is just a preview of the most popular features of AssemblyAI's API. If you want a full list of features, go check out our API documentation linked in the description below. And if you ever need some support, our team of developers is here to help. Everyday developers are using these features to build really exciting applications. From meeting summarizers to brand safety or contextual targeting platforms to full blown conversational intelligence tools. We can't wait to see what you build with AssemblyAI."

# Initialize normalizers
normalizer = EnglishTextNormalizer()
# For Spanish and other languages
# normalizer = BasicTextNormalizer()

def calculate_wer(reference, hypothesis, language='en'):
    # Normalize both texts
    normalized_reference = normalizer(reference)
    print("Reference: " + reference)
    print("Normalized Reference: " + normalized_reference + "\n")

    normalized_hypothesis = normalizer(hypothesis)
    print("Hypothesis: " + hypothesis)
    print("Normalized Hypothesis: " + normalized_hypothesis+ "\n")

    # Calculate WER
    wer = jiwer.wer(normalized_reference, normalized_hypothesis)

    return wer * 100  # Return as percentage

wer_score = calculate_wer(reference_transcript, assembly_streaming_transcript.strip())
print(f"Final WER: {wer_score:.2f}%")
