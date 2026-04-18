#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for OpenAI format requests.
"""

import requests
import json

BASE_URL = "http://localhost:9000"
API_KEY = "a"

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_models():
    """Test models list endpoint."""
    print("Testing /v1/models endpoint...")
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(f"{BASE_URL}/v1/models", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_chat_completion():
    """Test chat completion endpoint (non-streaming)."""
    print("Testing /v1/chat/completions endpoint (non-streaming)...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-3-flash",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is 2+2? Answer briefly."}
        ],
        "stream": False
    }
    response = requests.post(f"{BASE_URL}/v1/chat/completions", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_chat_completion_streaming():
    """Test chat completion endpoint (streaming)."""
    print("Testing /v1/chat/completions endpoint (streaming)...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-3-flash",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in 3 words."}
        ],
        "stream": True
    }
    response = requests.post(f"{BASE_URL}/v1/chat/completions", headers=headers, json=data, stream=True)
    print(f"Status: {response.status_code}")
    print("Streaming response:")
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("OpenAI Format Tests")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_models()
        test_chat_completion()
        test_chat_completion_streaming()
        print("✅ All OpenAI format tests completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
