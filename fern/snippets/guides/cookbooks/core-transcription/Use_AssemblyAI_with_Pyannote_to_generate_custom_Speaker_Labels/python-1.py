import os
import assemblyai as aai
from pyannote.audio import Pipeline
import torch
import pandas as pd
import numpy as np

# Assign your API keys
HUGGING_FACE_TOKEN = os.getenv("HF_TOKEN")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Authenticate with AssemblyAI
aai.settings.api_key = ASSEMBLYAI_API_KEY

def transcribe_audio(audio_file, language="en"):
    """
    Transcribe an audio file using AssemblyAI.

    Args:
        audio_file (str): Path to the audio file.
        language (str, optional): Language code for transcription. Defaults to "en".

    Returns:
        aai.Transcript: The transcription result.
    """

    transcriber = aai.Transcriber(config=aai.TranscriptionConfig(speech_model='nano', language_code=language))
    transcript = transcriber.transcribe(audio_file)
    print(f"Transcript ID: {transcript.id}")
    return transcript

def get_speaker_labels(audio_file, transcript: aai.Transcript):
    """
    Perform speaker diarization on an audio file and combine results with the transcript.

    Args:
        audio_file (str): Path to the audio file.
        transcript (aai.Transcript): The transcription result from AssemblyAI.

    Returns:
        str: A formatted string containing the transcript with speaker labels and timestamps.
    """
    # Initialize the speaker diarization pipeline with GPU support
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=HUGGING_FACE_TOKEN,
    )

    if pipeline is None:
        raise ValueError("Failed to initialize the pipeline. Please check your authentication token and internet connection.")
    else:
        pipeline = pipeline.to(device)

    # Apply the pipeline to the audio file
    diarization = pipeline(audio_file)

    # Create a dictionary to store speaker segments
    speaker_segments = {}

    # Process diarization results
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start, end = turn.start, turn.end
        if speaker not in speaker_segments:
            speaker_segments[speaker] = []
        speaker_segments[speaker].append((start, end))

    # Convert speaker_segments to a DataFrame
    diarize_df = pd.DataFrame([(speaker, start, end)
                               for speaker, segments in speaker_segments.items()
                               for start, end in segments],
                              columns=['speaker', 'start', 'end'])

    # Assign speakers to transcript words
    for word in transcript.words:
        word_start = float(word.start) / 1000
        word_end = float(word.end) / 1000

        overlaps = diarize_df[
            (diarize_df['start'] <= word_end) & (diarize_df['end'] >= word_start)
        ].copy()

        if not overlaps.empty:
            overlaps['overlap'] = np.minimum(overlaps['end'], word_end) - np.maximum(overlaps['start'], word_start)
            word.speaker = overlaps.loc[overlaps['overlap'].idxmax(), 'speaker']
        else:
            word.speaker = "Unknown"

    full_transcript = ''

    # Update segment speakers based on the majority speaker of its words
    for segment in transcript.get_sentences():
        segment_start = float(segment.start) / 1000
        segment_end = float(segment.end) / 1000

        overlaps = diarize_df[
            (diarize_df['start'] <= segment_end) & (diarize_df['end'] >= segment_start)
        ].copy()

        if not overlaps.empty:
            overlaps['overlap'] = np.minimum(overlaps['end'], segment_end) - np.maximum(overlaps['start'], segment_start)
            segment.speaker = overlaps.loc[overlaps['overlap'].idxmax(), 'speaker']
            speaker_label = segment.speaker.replace('SPEAKER_', 'SPEAKER ')
            full_transcript += f'[{format_timestamp(segment_start)}] {speaker_label}: {segment.text}\n'
        else:
            segment.speaker = "Unknown"
            full_transcript += f'[{format_timestamp(segment_start)}] Unknown: {segment.text}\n'

    return full_transcript

def format_timestamp(seconds):
    """
    Convert seconds to a formatted timestamp string (HH:MM:SS).

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted timestamp string.
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

audio_file = "audio.wav" # your local file path
transcript: aai.Transcript = transcribe_audio(audio_file, language="hr") # select a language code
transcript_with_speakers = get_speaker_labels(audio_file, transcript)
print(transcript_with_speakers)
