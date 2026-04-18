# -*- coding: utf-8 -*-

"""
Response converters for transforming Gemini responses to Anthropic format.
"""

import uuid
from typing import Dict, Any
from gemini.models_anthropic import (
    AnthropicResponse,
    AnthropicResponseContent,
    AnthropicUsage
)
from gemini.converters_openai import estimate_tokens


def convert_gemini_to_anthropic(gemini_response: Dict[str, Any], model: str, request_messages: list) -> Dict[str, Any]:
    """
    Convert Gemini API response to Anthropic message format.
    
    Args:
        gemini_response: Response from Gemini API
        model: Model name from request
        request_messages: Original request messages for token estimation
        
    Returns:
        Response in Anthropic format
    """
    # Extract text from Gemini response
    result = gemini_response.get("result", {})
    text = result.get("text", "")
    
    # Estimate tokens
    prompt_text = " ".join(str(msg.get("content", "")) for msg in request_messages)
    input_tokens = estimate_tokens(prompt_text)
    output_tokens = estimate_tokens(text)
    
    # Build Anthropic response
    response = AnthropicResponse(
        id=f"msg_{uuid.uuid4().hex[:24]}",
        type="message",
        role="assistant",
        content=[
            AnthropicResponseContent(
                type="text",
                text=text
            )
        ],
        model=model,
        stop_reason="end_turn",
        usage=AnthropicUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
    )
    
    return response.model_dump()


def create_anthropic_stream_event(text: str, event_type: str = "content_block_delta") -> str:
    """
    Create an Anthropic streaming event.
    
    Args:
        text: Text content for the event
        event_type: Type of event (content_block_delta, message_stop, etc.)
        
    Returns:
        Formatted SSE event
    """
    import json
    
    if event_type == "message_start":
        event = {
            "type": "message_start",
            "message": {
                "id": f"msg_{uuid.uuid4().hex[:24]}",
                "type": "message",
                "role": "assistant",
                "content": [],
                "model": "gemini-3-flash"
            }
        }
    elif event_type == "content_block_start":
        event = {
            "type": "content_block_start",
            "index": 0,
            "content_block": {
                "type": "text",
                "text": ""
            }
        }
    elif event_type == "content_block_delta":
        event = {
            "type": "content_block_delta",
            "index": 0,
            "delta": {
                "type": "text_delta",
                "text": text
            }
        }
    elif event_type == "content_block_stop":
        event = {
            "type": "content_block_stop",
            "index": 0
        }
    elif event_type == "message_delta":
        event = {
            "type": "message_delta",
            "delta": {
                "stop_reason": "end_turn"
            }
        }
    else:  # message_stop
        event = {
            "type": "message_stop"
        }
    
    return f"event: {event_type}\ndata: {json.dumps(event)}\n\n"
