# -*- coding: utf-8 -*-

"""
Unit tests for converter modules.
"""

import pytest
from gemini.converters_core import extract_text_content, estimate_tokens, build_gemini_prompt
from gemini.converters_openai import convert_openai_messages_to_unified, build_gemini_request
from gemini.models_openai import ChatMessage, ChatCompletionRequest


class TestConvertersCore:
    """Test core converter utilities."""
    
    def test_extract_text_content_string(self):
        """Test extracting text from string content."""
        content = "Hello, world!"
        result = extract_text_content(content)
        assert result == "Hello, world!"
    
    def test_extract_text_content_list(self):
        """Test extracting text from list content."""
        content = [
            {"type": "text", "text": "Hello"},
            {"type": "text", "text": "World"}
        ]
        result = extract_text_content(content)
        assert "Hello" in result
        assert "World" in result
    
    def test_extract_text_content_none(self):
        """Test extracting text from None."""
        result = extract_text_content(None)
        assert result == ""
    
    def test_estimate_tokens(self):
        """Test token estimation."""
        text = "Hello, world!"
        tokens = estimate_tokens(text)
        assert tokens > 0
        assert tokens == len(text) // 4
    
    def test_build_gemini_prompt(self):
        """Test building Gemini prompt from messages."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        prompt = build_gemini_prompt(messages)
        assert "User: Hello" in prompt
        assert "Assistant: Hi there!" in prompt
    
    def test_build_gemini_prompt_with_system(self):
        """Test building Gemini prompt with system message."""
        messages = [
            {"role": "user", "content": "Hello"}
        ]
        prompt = build_gemini_prompt(messages, system_prompt="You are helpful")
        assert "System: You are helpful" in prompt
        assert "User: Hello" in prompt


class TestConvertersOpenAI:
    """Test OpenAI converter functions."""
    
    def test_convert_openai_messages_basic(self):
        """Test converting basic OpenAI messages."""
        messages = [
            ChatMessage(role="system", content="You are helpful"),
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there!")
        ]
        
        system_prompt, unified = convert_openai_messages_to_unified(messages)
        
        assert "You are helpful" in system_prompt
        assert len(unified) == 2  # user and assistant, system extracted
        assert unified[0]["role"] == "user"
        assert unified[1]["role"] == "assistant"
    
    def test_build_gemini_request(self):
        """Test building Gemini request from OpenAI format."""
        request = ChatCompletionRequest(
            model="gemini-3-flash",
            messages=[
                ChatMessage(role="system", content="Be helpful"),
                ChatMessage(role="user", content="Hello")
            ]
        )
        
        gemini_params = build_gemini_request(request)
        
        assert "q" in gemini_params
        assert "inst" in gemini_params
        assert "Hello" in gemini_params["q"]
        assert "Be helpful" in gemini_params["inst"]
    
    def test_build_gemini_request_no_system(self):
        """Test building Gemini request without system message."""
        request = ChatCompletionRequest(
            model="gemini-3-flash",
            messages=[
                ChatMessage(role="user", content="Hello")
            ]
        )
        
        gemini_params = build_gemini_request(request)
        
        assert "q" in gemini_params
        assert "inst" in gemini_params
        assert gemini_params["inst"] == "jawab"  # Default instruction


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
