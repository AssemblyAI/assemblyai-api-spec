# AssemblyAI Transcripts API Specification

This directory contains the FastAPI-based API specification for AssemblyAI's Transcripts API, including automated testing and example generation.

## Overview

The transcripts API specification is built using:
- **FastAPI** for endpoint definitions and OpenAPI spec generation
- **Pydantic models** for request/response validation
- **Automated tests** that validate models against real API responses
- **Example generation** from live API calls for documentation

## Directory Structure

```
transcripts/
├── main.py              # FastAPI app with endpoint definitions
├── models.py            # Pydantic models for requests/responses
├── openapi.yml         # Generated OpenAPI specification
├── generate_spec.py    # Script to generate OpenAPI spec
├── example_loader.py   # Loads JSON examples into API docs
├── example_sanitizer.py # Sanitizes sensitive data in examples
├── examples/           # Real API response examples (JSON)
│   ├── transcript_create.json
│   ├── transcript_list.json
│   └── ...
└── tests/              # Test files that generate examples
    ├── test_endpoints.py
    ├── test_transcript.py
    └── test_features.py
```

## How It Works

### 1. Testing & Example Generation

The tests in `/tests` folder serve dual purposes:
- **Validate Pydantic models** against real AssemblyAI API responses
- **Generate example JSON files** for API documentation

```bash
# Run tests to generate examples and validate models
cd fern/apis/transcripts
uv run pytest tests/ -v
```

Each test:
1. Makes real API calls to AssemblyAI
2. Saves the JSON response as an example file
3. Validates the response using Pydantic models
4. **If validation fails**, it means the models need updating

### 2. Example Loading

The `example_loader.py` loads JSON examples into the FastAPI specification:

```python
# Examples are automatically included in OpenAPI responses
from example_loader import get_endpoint_examples
examples = get_endpoint_examples()
```

### 3. Sensitive Data Sanitization  

The `example_sanitizer.py` removes sensitive information (URLs, IDs) while preserving schema structure for documentation.

### 4. API Documentation

Examples appear in the generated API reference at `/docs/api-reference/transcripts/`

## Key Files

- **`main.py`**: FastAPI endpoints with descriptions copied from production OpenAPI spec
- **`models.py`**: Pydantic models matching AssemblyAI's API responses exactly
- **`tests/test_endpoints.py`**: Tests for all transcript endpoints
- **`examples/`**: Real API responses used as documentation examples

## Running Tests

```bash
# Set your API key
export ASSEMBLYAI_API_KEY=your_api_key_here

# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_endpoints.py -v
```

## Updating Models

If tests fail, it means the API response structure has changed:

1. Check the test output to see what field is missing/incorrect
2. Update the Pydantic models in `models.py`
3. Re-run tests to validate the fix
4. Regenerate the OpenAPI spec with `uv run python generate_spec.py`

## Generated Files

- **`openapi.yml`**: OpenAPI 3.1 specification with real examples
- **`examples/*.json`**: Real API responses for documentation