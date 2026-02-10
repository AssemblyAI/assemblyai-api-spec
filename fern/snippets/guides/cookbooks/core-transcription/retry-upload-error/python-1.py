import assemblyai as aai
import time
from assemblyai.types import TranscriptError

aai.settings.api_key = "YOUR_API_KEY"

def transcribe_with_upload_retry(file_path, retries=3, delay=5):
    transcriber = aai.Transcriber()

    for attempt in range(retries):
        try:
            # Attempt to transcribe the file
            config = aai.TranscriptionConfig(speaker_labels=True)
            transcript = transcriber.transcribe(file_path, config)
            return transcript

        except TranscriptError as e:
            # Handle specific error if upload fails
            print(f"Attempt {attempt + 1} failed. {e}")

            # Retry if a TranscriptError occurs,
            if attempt + 1 < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise e  # Raise the error after max retries

    print("Max retries reached. Transcription failed.")
    return None

transcribe_with_upload_retry("YOUR_AUDIO_URL")
