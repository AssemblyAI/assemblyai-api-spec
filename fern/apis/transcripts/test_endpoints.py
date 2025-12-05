"""
Test file for additional AssemblyAI endpoints beyond the main transcript endpoint.
These tests validate the actual API responses using our Pydantic models to ensure accuracy.
"""
import json
import os
import pytest
import requests
from pathlib import Path
from models import (
    TranscriptSentencesResponse,
    TranscriptParagraphsResponse,
    WordSearchResponse,
    RedactedAudioResponse,
    TranscriptListResponse,
    TranscriptResponse,
    TranscriptParams
)


class TestAssemblyAIEndpoints:
    """Test additional AssemblyAI endpoints by validating actual API responses."""
    
    def setup_method(self):
        """Setup for all test methods."""
        self.headers = {
            "authorization": os.getenv("ASSEMBLYAI_API_KEY")
        }
        self.base_url = "https://api.assemblyai.com/v2/transcript"
        self.transcript_id = "b6a5408c-caa1-4ba3-a866-1441a18f0cdb"
        
        # Create examples directory
        self.examples_dir = Path("examples")
        self.examples_dir.mkdir(exist_ok=True)
    
    def _save_example(self, filename, data):
        """Save JSON response as example file."""
        filepath = self.examples_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def test_get_sentences(self):
        """Test GET /v2/transcript/{transcript_id}/sentences endpoint using Pydantic model."""
        url = f"{self.base_url}/{self.transcript_id}/sentences"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        
        # Save example response
        self._save_example(f"{self.transcript_id}_sentences.json", data)

        TranscriptSentencesResponse.model_validate(data)
    
    def test_get_paragraphs(self):
        """Test GET /v2/transcript/{transcript_id}/paragraphs endpoint using Pydantic model."""
        url = f"{self.base_url}/{self.transcript_id}/paragraphs"
        
        response = requests.get(url, headers=self.headers)
        data = response.json()
        
        # Save example response
        self._save_example(f"{self.transcript_id}_paragraphs.json", data)

        TranscriptParagraphsResponse.model_validate(data)
    
    
    def test_get_redacted_audio(self):
        """Test GET /v2/transcript/{transcript_id}/redacted-audio endpoint."""
        # Use transcript ID that has PII redaction and redacted audio enabled
        redacted_transcript_id = "8c856a54-37a3-48db-9649-70a1a4127619"
        url = f"{self.base_url}/{redacted_transcript_id}/redacted-audio"
        
        response = requests.get(url, headers=self.headers)
        data = response.json()
        
        # Save example response
        self._save_example(f"{redacted_transcript_id}_redacted_audio.json", data)
        
        RedactedAudioResponse.model_validate(data)
    
    def test_get_word_search(self):
        """Test GET /v2/transcript/{transcript_id}/word-search endpoint using Pydantic model."""
        url = f"{self.base_url}/{self.transcript_id}/word-search"
        params = {"words": "the"}
        
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        
        # Save example response
        self._save_example(f"{self.transcript_id}_word_search.json", data)
        
        WordSearchResponse.model_validate(data)
    
    def test_delete_transcript(self):
        """Test DELETE /v2/transcript/{transcript_id} endpoint."""
        # Use an already deleted transcript ID to validate the response structure
        deleted_transcript_id = "08ff54b2-dc9e-4eba-83c1-c23e9364b45a"
        url = f"{self.base_url}/{deleted_transcript_id}"
        
        response = requests.get(url, headers=self.headers)
        data = response.json()
        
        # Save example response
        self._save_example(f"{deleted_transcript_id}_deleted.json", data)
        
        TranscriptResponse.model_validate(data)
    
    def test_transcript_list(self):
        """Test GET /v2/transcript endpoint (list transcripts) using Pydantic model."""
        url = f"{self.base_url}"
        
        params = {
            "limit": 10,
            "status": "completed"
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        
        # Save example response
        self._save_example("transcript_list.json", data)
        
        TranscriptListResponse.model_validate(data)
    
    def test_post_transcript(self):
        """Test POST /v2/transcript endpoint (create transcript) using Pydantic model."""
        url = f"{self.base_url}"
        
        # Create transcript params using the example audio URL
        transcript_params = {
            "audio_url": "https://assembly.ai/example.wav"
        }
        
        response = requests.post(url, headers=self.headers, json=transcript_params)
        data = response.json()
        
        # Save example response - this will be a "processing" or "queued" status
        self._save_example("transcript_create.json", data)
        
        TranscriptResponse.model_validate(data)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])