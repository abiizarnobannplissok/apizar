# -*- coding: utf-8 -*-

"""
Converter functions for transforming OpenAI format to Gemini format.
"""

from typing import Dict, List, Optional
from gemini.models_openai import ChatCompletionRequest, ChatMessage


def extract_system_and_user_messages(messages: List[ChatMessage]) -> tuple[str, str]:
    """
    Extract system instruction and user query from OpenAI messages.
    
    Args:
        messages: List of chat messages in OpenAI format
        
    Returns:
        Tuple of (system_instruction, user_query)
    """
    system_parts = []
    user_parts = []
    
    for msg in messages:
        content = msg.content if msg.content else ""
        
        if msg.role == "system":
            system_parts.append(content)
        elif msg.role == "user":
            user_parts.append(content)
        elif msg.role == "assistant":
            # Include assistant messages as context
            user_parts.append(f"Assistant previously said: {content}")
    
    # Combine all parts
    system_instruction = " ".join(system_parts) if system_parts else "You are a helpful assistant."
    user_query = " ".join(user_parts) if user_parts else "Hello"
    
    return system_instruction, user_query


def build_gemini_params(request: ChatCompletionRequest) -> Dict[str, str]:
    """
    Build Gemini API query parameters from OpenAI request.
    
    Args:
        request: OpenAI chat completion request
        
    Returns:
        Dictionary of query parameters for Gemini API
    """
    system_instruction, user_query = extract_system_and_user_messages(request.messages)
    
    return {
        "q": user_query,
        "inst": system_instruction
    }


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text.
    Simple estimation: ~4 characters per token.
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    return max(1, len(text) // 4)
