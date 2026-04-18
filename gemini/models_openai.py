# -*- coding: utf-8 -*-

"""
Pydantic models for OpenAI-compatible API.
"""

import time
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


# ==================================================================================================
# Models for /v1/models endpoint
# ==================================================================================================

class OpenAIModel(BaseModel):
    """Model information in OpenAI format."""
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "google"
    description: Optional[str] = None


class ModelList(BaseModel):
    """List of models in OpenAI format."""
    object: str = "list"
    data: List[OpenAIModel]


# ==================================================================================================
# Models for /v1/chat/completions endpoint
# ==================================================================================================

class ChatMessage(BaseModel):
    """Chat message in OpenAI format."""
    role: str
    content: Optional[Union[str, List[Any]]] = None
    name: Optional[str] = None
    
    model_config = {"extra": "allow"}


class ChatCompletionRequest(BaseModel):
    """Request for chat completion in OpenAI format."""
    model: str
    messages: List[ChatMessage]
    stream: bool = False
    temperature: Optional[float] = Field(default=1.0, ge=0, le=2)
    top_p: Optional[float] = Field(default=1.0, ge=0, le=1)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    stop: Optional[Union[str, List[str]]] = None
    
    model_config = {"extra": "allow"}


class ChatCompletionChoice(BaseModel):
    """Choice in chat completion response."""
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    """Token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """Response for chat completion."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage


class ChatCompletionChunk(BaseModel):
    """Streaming chunk for chat completion."""
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[Dict[str, Any]]
