# -*- coding: utf-8 -*-

"""
Streaming response handler for OpenAI format.
"""

import json
import uuid
from typing import AsyncGenerator, Dict, Any
from loguru import logger

from gemini.converters_core import estimate_tokens


async def stream_gemini_to_openai(
    gemini_response: str,
    model: str,
    request_id: str
) -> AsyncGenerator[str, None]:
    """
    Convert Gemini response to OpenAI streaming format.
    
    Args:
        gemini_response: Complete response text from Gemini API
        model: Model name to include in response
        request_id: Unique request ID
    
    Yields:
        SSE-formatted chunks in OpenAI format
    """
    # Send initial chunk with role
    initial_chunk = {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": int(__import__("time").time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {"role": "assistant", "content": ""},
            "finish_reason": None
        }]
    }
    yield f"data: {json.dumps(initial_chunk)}\n\n"
    
    # Stream content in chunks (simulate streaming for better UX)
    chunk_size = 50  # Characters per chunk
    for i in range(0, len(gemini_response), chunk_size):
        chunk_text = gemini_response[i:i + chunk_size]
        
        content_chunk = {
            "id": request_id,
            "object": "chat.completion.chunk",
            "created": int(__import__("time").time()),
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": chunk_text},
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(content_chunk)}\n\n"
    
    # Send final chunk with finish_reason
    final_chunk = {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": int(__import__("time").time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    
    # Send [DONE] marker
    yield "data: [DONE]\n\n"


def build_openai_response(
    gemini_response: str,
    model: str,
    request_id: str
) -> Dict[str, Any]:
    """
    Build complete OpenAI response from Gemini response.
    
    Args:
        gemini_response: Complete response text from Gemini API
        model: Model name to include in response
        request_id: Unique request ID
    
    Returns:
        Complete response in OpenAI format
    """
    # Estimate token counts
    completion_tokens = estimate_tokens(gemini_response)
    
    response = {
        "id": request_id,
        "object": "chat.completion",
        "created": int(__import__("time").time()),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": gemini_response
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 0,  # Gemini API doesn't provide this
            "completion_tokens": completion_tokens,
            "total_tokens": completion_tokens
        }
    }
    
    return response
