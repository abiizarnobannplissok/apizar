# -*- coding: utf-8 -*-

"""
Converter functions for transforming Anthropic format to Gemini format.
"""

from typing import Dict, List
from gemini.models_anthropic import AnthropicRequest, AnthropicMessage, ContentBlock


def extract_system_and_messages(request: AnthropicRequest) -> tuple[str, str]:
    """
    Extract system instruction and user query from Anthropic request.
    
    Args:
        request: Anthropic message request
        
    Returns:
        Tuple of (system_instruction, user_query)
    """
    # Use system field if provided
    system_instruction = request.system if request.system else "You are a helpful assistant."
    
    user_parts = []
    
    for msg in request.messages:
        # Handle content as string or list of content blocks
        if isinstance(msg.content, str):
            content_text = msg.content
        else:
            # Extract text from content blocks
            content_text = " ".join(
                block.text for block in msg.content 
                if hasattr(block, 'text') and block.text
            )
        
        if msg.role == "user":
            user_parts.append(content_text)
        elif msg.role == "assistant":
            # Include assistant messages as context
            user_parts.append(f"Assistant previously said: {content_text}")
    
    user_query = " ".join(user_parts) if user_parts else "Hello"
    
    return system_instruction, user_query


def build_gemini_params_from_anthropic(request: AnthropicRequest) -> Dict[str, str]:
    """
    Build Gemini API query parameters from Anthropic request.
    
    Args:
        request: Anthropic message request
        
    Returns:
        Dictionary of query parameters for Gemini API
    """
    system_instruction, user_query = extract_system_and_messages(request)
    
    return {
        "q": user_query,
        "inst": system_instruction
    }
