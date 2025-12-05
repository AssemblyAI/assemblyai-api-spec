"""
Example test file showing how to test different AssemblyAI features
by using transcripts with specific features enabled.

This demonstrates the TDD approach where tests will fail if the 
Pydantic models don't match the actual API schema.
"""
import json
import os
import pytest
import requests
from pathlib import Path
from models import TranscriptResponse


class TestAssemblyAIFeatures:
    """Test different AssemblyAI features by validating actual API responses."""
    
    def setup_method(self):
        """Setup for all test methods."""
        self.headers = {
            "authorization": os.getenv("ASSEMBLYAI_API_KEY")
        }
        self.base_url = "https://api.assemblyai.com/v2/transcript"
        
        # Create examples directory
        self.examples_dir = Path("examples")
        self.examples_dir.mkdir(exist_ok=True)
    
    def _save_example(self, filename, data):
        """Save JSON response as example file."""
        filepath = self.examples_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def test_basic_transcript(self):
        """Test basic transcript validation and required fields."""
        transcript_id = "b6a5408c-caa1-4ba3-a866-1441a18f0cdb"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        data = response.json()
        
        # Save example response
        self._save_example(f"{transcript_id}.json", data)
        
        TranscriptResponse.model_validate(data)
    
    def test_speaker_diarization(self):
        """Test transcript with speaker diarization enabled."""
        # Transcript with speaker_labels=true
        transcript_id = "b6a5408c-caa1-4ba3-a866-1441a18f0cdb"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        
        TranscriptResponse.model_validate(response.json())
    
    def test_sentiment_analysis(self):
        """Test transcript with sentiment analysis enabled."""
        # Transcript with sentiment_analysis=true
        transcript_id = "b6a5408c-caa1-4ba3-a866-1441a18f0cdb"
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        
        TranscriptResponse.model_validate(response.json())
    
    def test_auto_highlights(self):
        """Test transcript with auto highlights enabled."""
        transcript_id = "b6a5408c-caa1-4ba3-a866-1441a18f0cdb"
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        
        TranscriptResponse.model_validate(response.json())
    
    def test_content_moderation(self):
        """Test content moderation field validation."""
        transcript_id = "a78ccedc-224d-4ab6-b82e-277e345a1c55"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        TranscriptResponse.model_validate(response.json())
    
    def test_topic_detection(self):
        """Test topic detection field validation."""
        transcript_id = "a78ccedc-224d-4ab6-b82e-277e345a1c55"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        TranscriptResponse.model_validate(response.json())
    
    def test_entity_detection(self):
        """Test entity detection field validation."""
        transcript_id = "a78ccedc-224d-4ab6-b82e-277e345a1c55"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        TranscriptResponse.model_validate(response.json())
    
    def test_auto_chapters(self):
        """Test transcript with auto chapters enabled."""
        # Transcript with auto_chapters=true
        transcript_id = "b6a5408c-caa1-4ba3-a866-1441a18f0cdb"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        TranscriptResponse.model_validate(response.json())
    
    def test_summarization(self):
        """Test transcript with summarization enabled."""
        # You'll need a transcript ID with summarization=true
        transcript_id = "f3884d3c-dc5e-4203-8386-ef07327eb442"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        TranscriptResponse.model_validate(response.json())
    
    def test_pii_redaction(self):
        """Test transcript with PII redaction enabled."""
        transcript_id = "8c856a54-37a3-48db-9649-70a1a4127619"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        TranscriptResponse.model_validate(response.json())
    
    def test_multichannel(self):
        """Test transcript with multichannel audio."""
        # You'll need a transcript ID with multichannel=true
        transcript_id = "your-multichannel-transcript-id"
        
        response = requests.get(f"{self.base_url}/{transcript_id}", headers=self.headers)
        if response.status_code == 200:
            transcript = TranscriptResponse.model_validate(response.json())
            
            # Assertions for multichannel
            if transcript.multichannel:
                assert transcript.audio_channels is not None
                assert transcript.audio_channels > 1
                # Check that words have channel information
                if transcript.words:
                    channel_found = any(word.channel is not None for word in transcript.words)
                    assert channel_found, "Expected at least some words to have channel information"
        else:
            pytest.skip("Multichannel transcript not available for testing")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])