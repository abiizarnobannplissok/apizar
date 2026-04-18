#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for Anthropic format requests.
"""

import requests
import json

BASE_URL = "http://localhost:9000"
API_KEY = "a"

def test_messages():
    """Test messages endpoint (non-streaming)."""
    print("Testing /v1/messages endpoint (non-streaming)...")
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "gemini-3-flash",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "What is 2+2? Answer briefly."}
        ]
    }
    response = requests.post(f"{BASE_URL}/v1/messages", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_messages_with_system():
    """Test messages endpoint with system prompt."""
    print("Testing /v1/messages endpoint with system prompt...")
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "gemini-3-flash",
        "max_tokens": 1024,
        "system": "You are a helpful math tutor.",
        "messages": [
            {"role": "user", "content": "What is 5+5?"}
        ]
    }
    response = requests.post(f"{BASE_URL}/v1/messages", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_messages_streaming():
    """Test messages endpoint (streaming)."""
    print("Testing /v1/messages endpoint (streaming)...")
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "gemini-3-flash",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Say hello in 3 words."}
        ],
        "stream": True
    }
    response = requests.post(f"{BASE_URL}/v1/messages", headers=headers, json=data, stream=True)
    print(f"Status: {response.status_code}")
    print("Streaming response:")
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Anthropic Format Tests")
    print("=" * 60)
    print()
    
    try:
        test_messages()
        test_messages_with_system()
        test_messages_streaming()
        print("✅ All Anthropic format tests completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
