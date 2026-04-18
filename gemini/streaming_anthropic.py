# -*- coding: utf-8 -*-

"""
Streaming response handler for Anthropic format.
"""

import json
import uuid
from typing import AsyncGenerator, Dict, Any
from loguru import logger

from gemini.converters_core import estimate_tokens


async def stream_gemini_to_anthropic(
    gemini_response: str,
    model: str,
    request_id: str
) -> AsyncGenerator[str, None]:
    """
    Convert Gemini response to Anthropic streaming format.
    
    Args:
        gemini_response: Complete response text from Gemini API
        model: Model name to include in response
        request_id: Unique request ID
    
    Yields:
        SSE-formatted events in Anthropic format
    """
    # Send message_start event
    message_start = {
        "type": "message_start",
        "message": {
            "id": request_id,
            "type": "message",
            "role": "assistant",
            "content": [],
            "model": model,
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0
            }
        }
    }
    yield f"event: message_start\ndata: {json.dumps(message_start)}\n\n"
    
    # Send content_block_start event
    content_block_start = {
        "type": "content_block_start",
        "index": 0,
        "content_block": {
            "type": "text",
            "text": ""
        }
    }
    yield f"event: content_block_start\ndata: {json.dumps(content_block_start)}\n\n"
    
    # Stream content in chunks
    chunk_size = 50  # Characters per chunk
    for i in range(0, len(gemini_response), chunk_size):
        chunk_text = gemini_response[i:i + chunk_size]
        
        content_block_delta = {
            "type": "content_block_delta",
            "index": 0,
            "delta": {
                "type": "text_delta",
                "text": chunk_text
            }
        }
        yield f"event: content_block_delta\ndata: {json.dumps(content_block_delta)}\n\n"
    
    # Send content_block_stop event
    content_block_stop = {
        "type": "content_block_stop",
        "index": 0
    }
    yield f"event: content_block_stop\ndata: {json.dumps(content_block_stop)}\n\n"
    
    # Send message_delta event with usage
    completion_tokens = estimate_tokens(gemini_response)
    message_delta = {
        "type": "message_delta",
        "delta": {
            "stop_reason": "end_turn",
            "stop_sequence": None
        },
        "usage": {
            "output_tokens": completion_tokens
        }
    }
    yield f"event: message_delta\ndata: {json.dumps(message_delta)}\n\n"
    
    # Send message_stop event
    message_stop = {
        "type": "message_stop"
    }
    yield f"event: message_stop\ndata: {json.dumps(message_stop)}\n\n"


def build_anthropic_response(
    gemini_response: str,
    model: str,
    request_id: str
) -> Dict[str, Any]:
    """
    Build complete Anthropic response from Gemini response.
    
    Args:
        gemini_response: Complete response text from Gemini API
        model: Model name to include in response
        request_id: Unique request ID
    
    Returns:
        Complete response in Anthropic format
    """
    # Estimate token counts
    completion_tokens = estimate_tokens(gemini_response)
    
    response = {
        "id": request_id,
        "type": "message",
        "role": "assistant",
        "content": [{
            "type": "text",
            "text": gemini_response
        }],
        "model": model,
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {
            "input_tokens": 0,  # Gemini API doesn't provide this
            "output_tokens": completion_tokens
        }
    }
    
    return response
