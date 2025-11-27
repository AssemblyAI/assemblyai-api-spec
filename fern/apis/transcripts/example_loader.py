"""
Helper to load JSON examples from files for OpenAPI spec generation.
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any
from example_sanitizer import get_sanitized_examples


def load_example(filename: str) -> Optional[Dict[Any, Any]]:
    """Load a JSON example file if it exists."""
    examples_dir = Path("examples")
    filepath = examples_dir / filename
    
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    return None


def get_endpoint_examples():
    """Get all available endpoint examples with sanitized versions for sensitive endpoints."""
    # Load real examples for safe endpoints
    real_examples = {
        "transcript": load_example("b6a5408c-caa1-4ba3-a866-1441a18f0cdb.json"),
        "new_transcript": load_example("transcript_create.json"),
        "sentences": load_example("b6a5408c-caa1-4ba3-a866-1441a18f0cdb_sentences.json"),
        "paragraphs": load_example("b6a5408c-caa1-4ba3-a866-1441a18f0cdb_paragraphs.json"),
        "word_search": load_example("b6a5408c-caa1-4ba3-a866-1441a18f0cdb_word_search.json"),
        "deleted_transcript": load_example("08ff54b2-dc9e-4eba-83c1-c23e9364b45a_deleted.json"),
    }
    
    # Get sanitized examples for sensitive endpoints
    sanitized_examples = get_sanitized_examples()
    
    # Combine real and sanitized examples
    examples = {**real_examples, **sanitized_examples}
    
    # Filter out None values
    return {k: v for k, v in examples.items() if v is not None}