# -*- coding: utf-8 -*-

"""
Pydantic models for Anthropic-compatible API.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


# ==================================================================================================
# Models for /v1/messages endpoint
# ==================================================================================================

class ContentBlock(BaseModel):
    """Content block in Anthropic format."""
    type: str
    text: Optional[str] = None
    
    model_config = {"extra": "allow"}


class AnthropicMessage(BaseModel):
    """Message in Anthropic format."""
    role: str
    content: Union[str, List[ContentBlock]]


class AnthropicRequest(BaseModel):
    """Request for message generation in Anthropic format."""
    model: str
    messages: List[AnthropicMessage]
    max_tokens: int = Field(default=1024, ge=1)
    system: Optional[str] = None
    temperature: Optional[float] = Field(default=1.0, ge=0, le=1)
    top_p: Optional[float] = Field(default=None, ge=0, le=1)
    stream: bool = False
    stop_sequences: Optional[List[str]] = None
    
    model_config = {"extra": "allow"}


class AnthropicResponseContent(BaseModel):
    """Content in Anthropic response."""
    type: str = "text"
    text: str


class AnthropicUsage(BaseModel):
    """Token usage in Anthropic format."""
    input_tokens: int
    output_tokens: int


class AnthropicResponse(BaseModel):
    """Response for message generation in Anthropic format."""
    id: str
    type: str = "message"
    role: str = "assistant"
    content: List[AnthropicResponseContent]
    model: str
    stop_reason: Optional[str] = None
    usage: AnthropicUsage


class AnthropicStreamEvent(BaseModel):
    """Streaming event in Anthropic format."""
    type: str
    
    model_config = {"extra": "allow"}
