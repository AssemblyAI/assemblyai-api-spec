import assemblyai as aai
import asyncio
from typing import Dict, List
from assemblyai.types import (
    SpeakerOptions,
    LanguageDetectionOptions,
    PIIRedactionPolicy,
    PIISubstitutionPolicy,
)

# Configure API key
aai.settings.api_key = "your_api_key_here"

async def transcribe_meeting_async(audio_source: str) -> Dict:
    """
    Asynchronously transcribe a meeting recording with full features

    Args:
        audio_source: Either a local file path or publicly accessible URL
    """
    # Configure comprehensive meeting analysis
    config = aai.TranscriptionConfig(
        # Speaker diarization
        speaker_labels=True,
        speakers_expected=None,  # Use if you know exact number from Zoom/Meet/Teams
        speaker_options=SpeakerOptions(
            min_speakers_expected=2,
            max_speakers_expected=20
        ),  # Use if you know the min/max range
        multichannel=False,  # Set to True if audio has separate channel per speaker

        # Language detection
        language_detection=True,  # Auto-detect the most used language
        language_detection_options=LanguageDetectionOptions(
            code_switching=True,  # Preserve language switches
            code_switching_confidence_threshold=0.5,
        ),

        # Punctuation and formatting
        punctuate=True,
        format_text=True,

        # Boost accuracy of meeting-specific vocabulary
        keyterms_prompt=["quarterly", "KPI", "roadmap", "deliverables"],

        # Speech Understanding - commonly used models
        summarization=True,
        sentiment_analysis=True,
        entity_detection=True,
        redact_pii=True,
        redact_pii_policies=[
            PIIRedactionPolicy.person_name,
            PIIRedactionPolicy.organization,
            PIIRedactionPolicy.occupation,
        ],
        redact_pii_sub=PIISubstitutionPolicy.hash,
        redact_pii_audio=True
    )

    # Create transcriber
    transcriber = aai.Transcriber()

    try:
        # Submit transcription job
        transcript = await asyncio.to_thread(
            transcriber.transcribe,
            audio_source,
            config=config
        )

        # Check status
        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")

        # Process speaker-labeled utterances
        print("\n=== SPEAKER-LABELED TRANSCRIPT ===\n")

        for utterance in transcript.utterances:
            # Format timestamp
            start_time = utterance.start / 1000  # Convert to seconds
            end_time = utterance.end / 1000

            # Print formatted utterance
            print(f"[{start_time:.1f}s - {end_time:.1f}s] Speaker {utterance.speaker}:")
            print(f"  {utterance.text}")
            print(f"  Confidence: {utterance.confidence:.2%}\n")

        # Print summary data
        print("\n=== MEETING SUMMARY ===\n")
        print({
            "id": transcript.id,
            "status": transcript.status,
            "duration": transcript.audio_duration,
            "speaker_count": len(set(u.speaker for u in transcript.utterances)),
            "word_count": len(transcript.words) if transcript.words else 0,
            "detected_language": transcript.language_code if hasattr(transcript, 'language_code') else None,
            "summary": transcript.summary,
        })

        return {
            "transcript": transcript,
            "utterances": transcript.utterances,
            "summary": transcript.summary,
        }

    except Exception as e:
        print(f"Error during transcription: {e}")
        raise

async def main():
    """
    Example usage with error handling
    """
    # Use either local file OR URL (not both)
    audio_source = "https://assembly.ai/wildfires.mp3"  # Or "path/to/recording.mp3"

    try:
        result = await transcribe_meeting_async(audio_source)

        # Additional processing
        print(f"\nTotal speakers identified: {len(set(u.speaker for u in result['utterances']))}")
        print(f"Meeting duration: {result['transcript'].audio_duration} seconds")

    except Exception as e:
        print(f"Failed to process meeting: {e}")

if __name__ == "__main__":
    asyncio.run(main())
