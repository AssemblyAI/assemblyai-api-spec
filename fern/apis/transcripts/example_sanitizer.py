"""
Sanitizer for API response examples to remove sensitive information
while keeping the schema structure intact for OpenAPI generation.
"""
import json
import re
from typing import Dict, Any, List


def sanitize_url(url: str) -> str:
    """Sanitize URLs while keeping them realistic."""
    if "deleted_by_user" in url:
        return url  # Keep deleted URLs as-is
    if url.startswith("https://s3"):
        # Keep the S3 domain but sanitize the rest
        return "https://s3.us-west-2.amazonaws.com/api.assembly.ai.usw2/redacted-audio/transcript-id.mp3?AWSAccessKeyId=EXAMPLE&Signature=EXAMPLE..."
    # Use AssemblyAI's example audio URL
    return "https://assembly.ai/nbc.mp3"


def sanitize_transcript_list_from_real(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize transcript list by only changing sensitive URLs, keeping real structure."""
    if not data:
        return data
        
    sanitized = data.copy()
    
    # Sanitize transcript items - only change audio URLs
    if "transcripts" in sanitized and sanitized["transcripts"]:
        sanitized_transcripts = []
        for transcript in sanitized["transcripts"]:
            sanitized_transcript = transcript.copy()
            # Only sanitize the audio_url, keep everything else real
            if "audio_url" in sanitized_transcript:
                sanitized_transcript["audio_url"] = sanitize_url(transcript["audio_url"])
            sanitized_transcripts.append(sanitized_transcript)
        
        sanitized["transcripts"] = sanitized_transcripts
    
    return sanitized


def sanitize_redacted_audio_from_real(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize redacted audio response by only changing the presigned URL."""
    if not data:
        return data
        
    sanitized = data.copy()
    if "redacted_audio_url" in sanitized:
        sanitized["redacted_audio_url"] = sanitize_url(sanitized["redacted_audio_url"])
    return sanitized


def get_sanitized_examples() -> Dict[str, Dict[str, Any]]:
    """Get sanitized examples by loading real data and sanitizing sensitive parts."""
    from pathlib import Path
    import json
    
    examples_dir = Path("examples")
    sanitized = {}
    
    # Sanitize transcript list
    transcript_list_file = examples_dir / "transcript_list.json"
    if transcript_list_file.exists():
        try:
            with open(transcript_list_file, 'r') as f:
                data = json.load(f)
            sanitized["transcript_list"] = sanitize_transcript_list_from_real(data)
        except (json.JSONDecodeError, IOError):
            pass
    
    # Sanitize redacted audio
    redacted_audio_file = examples_dir / "8c856a54-37a3-48db-9649-70a1a4127619_redacted_audio.json"
    if redacted_audio_file.exists():
        try:
            with open(redacted_audio_file, 'r') as f:
                data = json.load(f)
            sanitized["redacted_audio"] = sanitize_redacted_audio_from_real(data)
        except (json.JSONDecodeError, IOError):
            pass
    
    return sanitized