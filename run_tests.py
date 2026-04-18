#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive test script for Gemini Gateway.
Starts server, runs tests, and stops server.
"""

import subprocess
import time
import requests
import json
import sys
import signal

SERVER_PORT = 9000
BASE_URL = f"http://localhost:{SERVER_PORT}"
API_KEY = "a"

server_process = None

def start_server():
    """Start the Gemini Gateway server."""
    global server_process
    print("Starting Gemini Gateway server...")
    server_process = subprocess.Popen(
        ["./venv/bin/python", "main.py", "--port", str(SERVER_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/media/abiizar/DATA/snowping/gemini_gateway"
    )
    time.sleep(3)  # Wait for server to start
    print(f"Server started on port {SERVER_PORT}\n")

def stop_server():
    """Stop the Gemini Gateway server."""
    global server_process
    if server_process:
        print("\nStopping server...")
        server_process.send_signal(signal.SIGTERM)
        server_process.wait(timeout=5)
        print("Server stopped.")

def test_health():
    """Test health endpoint."""
    print("=" * 60)
    print("TEST: Health Endpoint")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ PASSED\n")

def test_openai_models():
    """Test OpenAI models endpoint."""
    print("=" * 60)
    print("TEST: OpenAI /v1/models")
    print("=" * 60)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{BASE_URL}/v1/models", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ PASSED\n")

def test_openai_chat():
    """Test OpenAI chat completions."""
    print("=" * 60)
    print("TEST: OpenAI /v1/chat/completions (non-streaming)")
    print("=" * 60)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-3-flash",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is 2+2? Answer in one word."}
        ],
        "stream": False
    }
    response = requests.post(f"{BASE_URL}/v1/chat/completions", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 200
    assert "choices" in result
    assert len(result["choices"]) > 0
    print(f"\n💬 Assistant response: {result['choices'][0]['message']['content']}")
    print("✅ PASSED\n")

def test_openai_streaming():
    """Test OpenAI streaming."""
    print("=" * 60)
    print("TEST: OpenAI /v1/chat/completions (streaming)")
    print("=" * 60)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-3-flash",
        "messages": [
            {"role": "user", "content": "Say 'Hello World'"}
        ],
        "stream": True
    }
    response = requests.post(f"{BASE_URL}/v1/chat/completions", headers=headers, json=data, stream=True)
    print(f"Status: {response.status_code}")
    print("Streaming chunks:")
    chunk_count = 0
    for line in response.iter_lines():
        if line:
            chunk_count += 1
            print(f"  {line.decode('utf-8')[:100]}")
    assert response.status_code == 200
    assert chunk_count > 0
    print(f"Received {chunk_count} chunks")
    print("✅ PASSED\n")

def test_anthropic_messages():
    """Test Anthropic messages endpoint."""
    print("=" * 60)
    print("TEST: Anthropic /v1/messages (non-streaming)")
    print("=" * 60)
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "gemini-3-flash",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "What is 3+3? Answer in one word."}
        ]
    }
    response = requests.post(f"{BASE_URL}/v1/messages", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 200
    assert "content" in result
    assert len(result["content"]) > 0
    print(f"\n💬 Assistant response: {result['content'][0]['text']}")
    print("✅ PASSED\n")

def test_anthropic_streaming():
    """Test Anthropic streaming."""
    print("=" * 60)
    print("TEST: Anthropic /v1/messages (streaming)")
    print("=" * 60)
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "gemini-3-flash",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Say 'Hello World'"}
        ],
        "stream": True
    }
    response = requests.post(f"{BASE_URL}/v1/messages", headers=headers, json=data, stream=True)
    print(f"Status: {response.status_code}")
    print("Streaming events:")
    event_count = 0
    for line in response.iter_lines():
        if line:
            event_count += 1
            print(f"  {line.decode('utf-8')[:100]}")
    assert response.status_code == 200
    assert event_count > 0
    print(f"Received {event_count} events")
    print("✅ PASSED\n")

if __name__ == "__main__":
    try:
        start_server()
        
        print("\n" + "=" * 60)
        print("GEMINI GATEWAY TEST SUITE")
        print("=" * 60 + "\n")
        
        # Run all tests
        test_health()
        test_openai_models()
        test_openai_chat()
        test_openai_streaming()
        test_anthropic_messages()
        test_anthropic_streaming()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        stop_server()
