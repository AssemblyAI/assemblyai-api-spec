from fastapi import FastAPI, Query, Security, File, UploadFile
from fastapi.security import APIKeyHeader
from typing import Optional
from models import (
    TranscriptResponse,
    TranscriptSentencesResponse,
    TranscriptParagraphsResponse,
    WordSearchResponse,
    RedactedAudioResponse,
    TranscriptListResponse,
    SubtitleFormat,
    ErrorResponse,
    UploadedFile,
    TranscriptParams,
)
from example_loader import get_endpoint_examples

security = APIKeyHeader(name="Authorization", description="AssemblyAI API Key")

# Load real API response examples
examples = get_endpoint_examples()

app = FastAPI(
    title="AssemblyAI API",
    version="1.3.4",
    description="AssemblyAI API",
    contact={
        "name": "API Support",
        "email": "support@assemblyai.com",
        "url": "https://www.assemblyai.com/docs/",
    },
    terms_of_service="https://www.assemblyai.com/legal/terms-of-service",
    servers=[
        {
            "url": "https://api.assemblyai.com",
            "description": "US server"
        },
        {
            "url": "https://api.eu.assemblyai.com", 
            "description": "EU server"
        }
    ]
)


@app.post(
    "/v2/transcript",
    response_model=TranscriptResponse,
    summary="Create transcript",
    description="Create a transcript from a media file. The transcript is queued for processing and will be available when the status is 'completed'.",
    operation_id="createTranscript",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Transcript created successfully",
            "content": {
                "application/json": {
                    "example": examples.get("new_transcript")
                }
            }
        },
        400: {
            "description": "Bad Request - Invalid parameters",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"error": "audio_url is required"}
                }
            }
        }
    } if examples.get("new_transcript") else {}
)
async def create_transcript(params: TranscriptParams, token: str = Security(security)):
    """
    Create a transcript.
    
    Submits a transcription job using the provided parameters. Returns the transcript
    object with status 'queued' or 'processing'. Use GET /v2/transcript/{transcript_id}
    to check the status and retrieve the completed transcript.
    """
    pass


@app.get(
    "/v2/transcript/{transcript_id}",
    response_model=TranscriptResponse,
    summary="Get transcript",
    description='Get the transcript resource. The transcript is ready when the "status" is "completed".',
    operation_id="getTranscript",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"example": examples.get("transcript")}},
        }
    }
    if examples.get("transcript")
    else {},
)
async def get_transcript(transcript_id: str, token: str = Security(security)):
    """
    Get transcript by ID.

    This endpoint generates the OpenAPI specification that matches AssemblyAI's actual API.
    The response model has been validated against real API responses for accuracy.
    """
    pass


@app.get(
    "/v2/transcript/{transcript_id}/sentences",
    response_model=TranscriptSentencesResponse,
    summary="Get transcript sentences",
    description="Get sentences of the transcript. Each sentence includes timing information and the words that make up the sentence.",
    operation_id="getTranscriptSentences",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"example": examples.get("sentences")}},
        }
    }
    if examples.get("sentences")
    else {},
)
async def get_transcript_sentences(transcript_id: str, token: str = Security(security)):
    """
    Get transcript sentences.

    Returns an array of sentence objects with timing information and word-level details.
    """
    pass


@app.get(
    "/v2/transcript/{transcript_id}/paragraphs",
    response_model=TranscriptParagraphsResponse,
    summary="Get transcript paragraphs",
    description="Get paragraphs of the transcript. Each paragraph includes timing information and the words that make up the paragraph.",
    operation_id="getTranscriptParagraphs",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"example": examples.get("paragraphs")}},
        }
    }
    if examples.get("paragraphs")
    else {},
)
async def get_transcript_paragraphs(
    transcript_id: str, token: str = Security(security)
):
    """
    Get transcript paragraphs.

    Returns an array of paragraph objects with timing information and word-level details.
    """
    pass


@app.get(
    "/v2/transcript/{transcript_id}/{subtitle_format}",
    summary="Get subtitles for transcript",
    description="Export your transcript in SRT or VTT format to use with a video player for subtitles and closed captions.",
    operation_id="getSubtitles",
    tags=["transcripts"],
    responses={
        200: {
            "description": "The exported captions as text",
            "content": {
                "text/plain": {
                    "schema": {"type": "string"},
                    "examples": {
                        "srt": {
                            "summary": "SRT format example",
                            "value": "1\n00:00:00,240 --> 00:00:11,040\nSmoke from hundreds of wildfires in Canada is triggering air quality alerts...\n\n2\n00:00:11,040 --> 00:00:16,220\nthroughout the US Skylines from Maine to Maryland to Minnesota are gray...",
                        },
                        "vtt": {
                            "summary": "VTT format example",
                            "value": "WEBVTT\n\n00:00:00.240 --> 00:00:11.040\nSmoke from hundreds of wildfires in Canada is triggering air quality alerts...\n\n00:00:11.040 --> 00:00:16.220\nthroughout the US Skylines from Maine to Maryland to Minnesota are gray...",
                        },
                    },
                }
            },
        }
    },
)
async def get_subtitles(
    transcript_id: str,
    subtitle_format: SubtitleFormat,
    chars_per_caption: Optional[int] = Query(
        None, description="The maximum number of characters per caption"
    ),
    token: str = Security(security),
):
    """
    Export transcript as subtitle file.

    Returns the transcript formatted as either an SRT or VTT subtitle file depending on the format specified.
    Optionally limits the number of characters per caption line.
    """
    pass


@app.get(
    "/v2/transcript/{transcript_id}/word-search",
    response_model=WordSearchResponse,
    summary="Search for words in transcript",
    description="Search for specific words or phrases in the transcript and get their timestamps.",
    operation_id="wordSearch",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"example": examples.get("word_search")}},
        }
    }
    if examples.get("word_search")
    else {},
)
async def search_transcript_words(
    transcript_id: str,
    words: str = Query(
        ..., description="The word or phrase to search for in the transcript"
    ),
    token: str = Security(security),
):
    """
    Search for words in the transcript.

    Returns locations and timestamps where the specified words or phrases appear.
    """
    pass


@app.get(
    "/v2/transcript/{transcript_id}/redacted-audio",
    response_model=RedactedAudioResponse,
    summary="Get redacted audio URL",
    description="Retrieve the URL of the redacted audio file if PII redaction was enabled during transcription.",
    operation_id="getRedactedAudio",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Redacted audio URL retrieved successfully",
            "model": RedactedAudioResponse,
            "content": {
                "application/json": {"example": examples.get("redacted_audio")}
            },
        },
        400: {
            "description": "Bad Request - Various errors including transcript not found, PII redaction not enabled, or transcript still processing",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "examples": {
                        "transcript_not_found": {
                            "summary": "Transcript not found",
                            "value": {
                                "error": "Transcript lookup error, transcript id not found"
                            },
                        },
                        "no_redacted_audio": {
                            "summary": "PII redaction not enabled",
                            "value": {
                                "error": "A redacted audio file for this transcript ID doesn't exist. Try submitting the transcript again with `redact_pii_audio` set to `true`."
                            },
                        },
                        "still_processing": {
                            "summary": "Transcript still processing",
                            "value": {
                                "error": "Transcription is still in progress. Redacted audio will be available after it has completed."
                            },
                        },
                    }
                }
            },
        },
    },
)
async def get_redacted_audio(transcript_id: str, token: str = Security(security)):
    """
    Get redacted audio file URL.

    Returns the URL of the audio file with PII (Personally Identifiable Information) redacted.
    Only available if PII redaction was enabled during transcription.
    """
    pass


@app.get(
    "/v2/transcript",
    response_model=TranscriptListResponse,
    summary="List transcripts",
    description="Get a list of transcripts you created.",
    operation_id="listTranscripts",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {"example": examples.get("transcript_list")}
            },
        }
    }
    if examples.get("transcript_list")
    else {},
)
async def list_transcripts(
    limit: Optional[int] = Query(
        None, description="Maximum amount of transcripts to retrieve", ge=1, le=200
    ),
    status: Optional[str] = Query(None, description="Filter by transcript status"),
    created_on: Optional[str] = Query(
        None, description="Get transcripts created on this date"
    ),
    before_id: Optional[str] = Query(
        None, description="Get transcripts that were created before this transcript ID"
    ),
    after_id: Optional[str] = Query(
        None, description="Get transcripts that were created after this transcript ID"
    ),
    token: str = Security(security),
):
    """
    List transcripts.

    Returns a paginated list of transcripts with optional filtering by status and date.
    """
    pass


@app.delete(
    "/v2/transcript/{transcript_id}",
    response_model=TranscriptResponse,
    summary="Delete transcript",
    description="Remove the data from the transcript and mark it as deleted. Returns the transcript with is_deleted=true and sanitized fields.",
    operation_id="deleteTranscript",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Transcript deleted successfully",
            "model": TranscriptResponse,
            "content": {
                "application/json": {"example": examples.get("deleted_transcript")}
            },
        },
        400: {
            "description": "Bad Request - Transcript not found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "Transcript lookup error, transcript id not found"
                    }
                }
            },
        },
    },
)
async def delete_transcript(transcript_id: str, token: str = Security(security)):
    """
    Delete a transcript.

    Removes the transcript data and marks it as deleted. Sensitive information is sanitized
    and the transcript is marked with is_deleted=true.
    """
    pass


@app.post(
    "/v2/upload",
    response_model=UploadedFile,
    summary="Upload a media file",
    description="Upload a media file to AssemblyAI's servers.",
    operation_id="uploadFile",
    tags=["transcripts"],
    responses={
        200: {
            "description": "Media file uploaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "upload_url": "https://cdn.assemblyai.com/upload/f756988d-47e2-4ca3-96ce-04bb168f8f2a"
                    }
                }
            }
        }
    }
)
async def upload_file(file: bytes = File(...), token: str = Security(security)):
    """
    Upload a media file.
    
    Uploads binary data (application/octet-stream) and returns a URL that can be used
    for transcript creation. The URL is accessible only by AssemblyAI's servers.
    """
    pass
