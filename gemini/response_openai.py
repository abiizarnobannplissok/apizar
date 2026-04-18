# -*- coding: utf-8 -*-

"""
Response converters for transforming Gemini responses to OpenAI format.
"""

import time
import uuid
from typing import Dict, Any
from gemini.models_openai import (
    ChatCompletionResponse,
    ChatCompletionChoice,
    ChatMessage,
    Usage
)
from gemini.converters_openai import estimate_tokens


def convert_gemini_to_openai(gemini_response: Dict[str, Any], model: str, request_messages: list) -> Dict[str, Any]:
    """
    Convert Gemini API response to OpenAI chat completion format.
    
    Args:
        gemini_response: Response from Gemini API
        model: Model name from request
        request_messages: Original request messages for token estimation
        
    Returns:
        Response in OpenAI format
    """
    # Extract text from Gemini response
    result = gemini_response.get("result", {})
    text = result.get("text", "")
    
    # Estimate tokens
    prompt_text = " ".join(str(msg.get("content", "")) for msg in request_messages)
    prompt_tokens = estimate_tokens(prompt_text)
    completion_tokens = estimate_tokens(text)
    
    # Build OpenAI response
    response = ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:8]}",
        object="chat.completion",
        created=int(time.time()),
        model=model,
        choices=[
            ChatCompletionChoice(
                index=0,
                message=ChatMessage(
                    role="assistant",
                    content=text
                ),
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    )
    
    return response.model_dump()


def create_openai_stream_chunk(text: str, model: str, is_final: bool = False) -> str:
    """
    Create an OpenAI streaming chunk.
    
    Args:
        text: Text content for the chunk
        model: Model name
        is_final: Whether this is the final chunk
        
    Returns:
        Formatted SSE chunk
    """
    chunk_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
    
    if is_final:
        chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }
            ]
        }
    else:
        chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant",
                        "content": text
                    },
                    "finish_reason": None
                }
            ]
        }
    
    import json
    return f"data: {json.dumps(chunk)}\n\n"
