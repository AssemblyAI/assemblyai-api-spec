import os
import requests
from models import TranscriptResponse


def test_assemblyai_transcript_schema():
    """Test that our TranscriptResponse model can parse actual AssemblyAI API responses"""
    # Use a real transcript ID from AssemblyAI production API
    # You'll need to replace this with an actual transcript ID from your AssemblyAI account
    transcript_id = "a78ccedc-224d-4ab6-b82e-277e345a1c55"
    
    # Make request to actual AssemblyAI API
    headers = {
        "authorization": os.getenv("ASSEMBLYAI_API_KEY")
    }
    
    response = requests.get(
        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
        headers=headers
    )
    
    assert response.status_code == 200
    
    # Debug: print the response to see nested structure (comment out for cleaner output)
    # import json
    # print("API Response:")
    # print(json.dumps(response.json(), indent=2))
    
    # This will fail if our Pydantic model doesn't match the actual API response schema
    transcript = TranscriptResponse.model_validate(response.json())
    
    # Basic assertions to verify we got valid data
    assert transcript.id == transcript_id
    assert transcript.status in ["queued", "processing", "completed", "error"]