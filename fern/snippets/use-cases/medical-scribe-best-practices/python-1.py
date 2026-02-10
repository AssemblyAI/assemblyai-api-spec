import assemblyai as aai
import asyncio
from typing import Dict, List
from assemblyai.types import (
    SpeakerOptions,
    PIIRedactionPolicy,
    PIISubstitutionPolicy,
)

# Configure API key
aai.settings.api_key = "your_api_key_here"

async def transcribe_encounter_async(audio_source: str) -> Dict:
    """
    Asynchronously transcribe a medical encounter with Universal-3-Pro

    Args:
        audio_source: Either a local file path or publicly accessible URL
    """
    # Configure comprehensive medical transcription
    config = aai.TranscriptionConfig(
        speech_model=aai.SpeechModel.universal_3_pro,

        # Diarize provider and patient
        speaker_labels=True,
        speakers_expected=2,  # Typically provider and patient

        # Punctuation and Formatting
        punctuate=True,
        format_text=True,

        # Boost accuracy of medical terminology
        keyterms_prompt=[
            # Patient-specific context
            "hypertension", "diabetes mellitus type 2", "metformin",

            # Specialty-specific terms
            "auscultation", "palpation", "differential diagnosis",
            "chief complaint", "review of systems", "physical examination",

            # Common medications
            "lisinopril", "atorvastatin", "levothyroxine",

            # Procedure terms
            "electrocardiogram", "complete blood count", "hemoglobin A1c"
        ],

        # Speech understanding for medical documentation
        entity_detection=True,  # Extract medications, conditions, procedures
        redact_pii=True,  # HIPAA compliance
        redact_pii_policies=[
            PIIRedactionPolicy.person_name,
            PIIRedactionPolicy.date_of_birth,
            PIIRedactionPolicy.phone_number,
            PIIRedactionPolicy.email_address,
        ],
        redact_pii_sub=PIISubstitutionPolicy.hash,
        redact_pii_audio=True  # Create HIPAA-compliant audio
    )

    # Create async transcriber
    transcriber = aai.Transcriber()

    try:
        # Submit transcription job - works with both file paths and URLs
        transcript = await asyncio.to_thread(
            transcriber.transcribe,
            audio_source,
            config=config
        )

        # Check status
        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")

        # Process speaker-labeled utterances
        print("\n=== PROVIDER-PATIENT DIALOGUE ===\n")

        for utterance in transcript.utterances:
            # Format timestamp
            start_time = utterance.start / 1000  # Convert to seconds
            end_time = utterance.end / 1000

            # Identify speaker role
            speaker_label = "Provider" if utterance.speaker == "A" else "Patient"

            # Print formatted utterance
            print(f"[{start_time:.1f}s - {end_time:.1f}s] {speaker_label}:")
            print(f"  {utterance.text}")
            print(f"  Confidence: {utterance.confidence:.2%}\n")

        # Extract clinical entities
        if transcript.entities:
            print("\n=== CLINICAL ENTITIES DETECTED ===\n")
            medications = [e for e in transcript.entities if e.entity_type == "medication"]
            conditions = [e for e in transcript.entities if e.entity_type == "medical_condition"]
            procedures = [e for e in transcript.entities if e.entity_type == "medical_procedure"]

            if medications:
                print("Medications:", ", ".join([m.text for m in medications]))
            if conditions:
                print("Conditions:", ", ".join([c.text for c in conditions]))
            if procedures:
                print("Procedures:", ", ".join([p.text for p in procedures]))

        return {
            "transcript": transcript,
            "utterances": transcript.utterances,
            "entities": transcript.entities,
            "redacted_audio_url": transcript.redacted_audio_url
        }

    except Exception as e:
        print(f"Error during transcription: {e}")
        raise

async def main():
    """
    Example usage for medical encounter
    """
    # Can use either local file or URL
    audio_source = "path/to/patient_encounter.mp3"  # Or use URL
    # audio_source = "https://your-secure-storage.com/encounter.mp3"

    try:
        result = await transcribe_encounter_async(audio_source)

        # Additional processing
        print(f"\nEncounter duration: {result['transcript'].audio_duration} seconds")

        # Could send to LLM Gateway for SOAP note generation here

    except Exception as e:
        print(f"Failed to process encounter: {e}")

if __name__ == "__main__":
    asyncio.run(main())
