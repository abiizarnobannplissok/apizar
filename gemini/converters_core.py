# -*- coding: utf-8 -*-

"""
Core converter utilities for Gemini Gateway.

Shared functions for message and content processing.
"""

from typing import Any, Dict, List, Optional
from loguru import logger


def extract_text_content(content: Any) -> str:
    """
    Extract text from various content formats.
    
    Args:
        content: Content in various formats (string, list, dict)
    
    Returns:
        Extracted text as string
    """
    if content is None:
        return ""
    
    if isinstance(content, str):
        return content
    
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif "text" in item:
                    text_parts.append(item["text"])
            elif isinstance(item, str):
                text_parts.append(item)
        return " ".join(text_parts)
    
    if isinstance(content, dict):
        if content.get("type") == "text":
            return content.get("text", "")
        if "text" in content:
            return content["text"]
    
    return str(content)


def build_gemini_prompt(
    messages: List[Dict[str, Any]],
    system_prompt: Optional[str] = None
) -> str:
    """
    Build a single prompt string from messages for Gemini API.
    
    The Gemini API expects a simple query string, so we need to
    combine all messages into a coherent prompt.
    
    Args:
        messages: List of messages in unified format
        system_prompt: Optional system prompt to prepend
    
    Returns:
        Combined prompt string
    """
    prompt_parts = []
    
    # Add system prompt if provided
    if system_prompt:
        prompt_parts.append(f"System: {system_prompt}")
    
    # Process messages
    for msg in messages:
        role = msg.get("role", "user")
        content = extract_text_content(msg.get("content", ""))
        
        if role == "system":
            prompt_parts.append(f"System: {content}")
        elif role == "user":
            prompt_parts.append(f"User: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")
        elif role == "tool":
            # Tool results as user messages
            prompt_parts.append(f"Tool Result: {content}")
    
    return "\n\n".join(prompt_parts)


def estimate_tokens(text: str) -> int:
    """
    Estimate token count from text.
    
    Simple estimation: ~4 characters per token for English text.
    
    Args:
        text: Input text
    
    Returns:
        Estimated token count
    """
    if not text:
        return 0
    
    # Simple heuristic: 4 chars ≈ 1 token
    return max(1, len(text) // 4)
