from fastapi import FastAPI, Security
from fastapi.security import APIKeyHeader
from models import (
    ChatCompletionsRequest,
    ChatCompletionsResponse,
    UnderstandingRequest,
    UnderstandingResponse,
    DeleteResponse,
)

security = APIKeyHeader(name="Authorization", description="AssemblyAI API Key")

app = FastAPI(
    title="AssemblyAI LLM Gateway API",
    version="1.0.0",
    description="AssemblyAI LLM Gateway API",
    contact={
        "name": "API Support",
        "email": "support@assemblyai.com",
        "url": "https://www.assemblyai.com/docs/",
    },
    terms_of_service="https://www.assemblyai.com/legal/terms-of-service",
    servers=[
        {
            "url": "https://llm-gateway.assemblyai.com",
            "description": "LLM Gateway server",
        }
    ],
)


@app.post(
    "/v1/chat/completions",
    response_model=ChatCompletionsResponse,
    summary="Create chat completion",
    description="Generate a chat completion using the specified model.",
    operation_id="createChatCompletion",
    tags=["chat"],
)
async def create_chat_completion(
    request: ChatCompletionsRequest, token: str = Security(security)
):
    """
    Create a chat completion.

    Generate a text completion using the specified model and parameters.
    """
    pass


@app.post(
    "/v1/understanding",
    response_model=UnderstandingResponse,
    summary="Process speech understanding",
    description="Apply speech understanding features to a transcript.",
    operation_id="processUnderstanding",
    tags=["understanding"],
)
async def process_understanding(
    request: UnderstandingRequest, token: str = Security(security)
):
    """
    Process speech understanding features.

    Apply speech understanding features like speaker identification to a transcript.
    """
    pass


@app.delete(
    "/v1/chat/completions/{request_id}",
    response_model=DeleteResponse,
    summary="Delete chat completion request",
    description="Cancel or delete a chat completion request by ID.",
    operation_id="deleteChatCompletion",
    tags=["chat"],
)
async def delete_chat_completion(request_id: str, token: str = Security(security)):
    """
    Delete a chat completion request.

    Cancel or delete a specific chat completion request using its unique ID.
    """
    pass
