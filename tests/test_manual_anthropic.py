# -*- coding: utf-8 -*-

"""
Manual test script for Anthropic-compatible API.

Run this script to test the gateway with Anthropic format.
"""

import asyncio
import httpx


async def test_anthropic_api():
    """Test Anthropic-compatible endpoints."""
    base_url = "http://localhost:6000"
    api_key = "gemini-secret-key-123"
    
    print("=" * 60)
    print("Testing Gemini Gateway - Anthropic API")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Test 1: Health check
        print("\n1. Testing health check...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 2: Messages (non-streaming)
        print("\n2. Testing /v1/messages (non-streaming)...")
        try:
            response = await client.post(
                f"{base_url}/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-3-flash",
                    "max_tokens": 1024,
                    "messages": [
                        {"role": "user", "content": "Say hello in 5 words"}
                    ]
                }
            )
            print(f"   Status: {response.status_code}")
            result = response.json()
            if "content" in result:
                print(f"   Response: {result['content'][0]['text']}")
            else:
                print(f"   Response: {result}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 3: Messages with system prompt
        print("\n3. Testing /v1/messages with system prompt...")
        try:
            response = await client.post(
                f"{base_url}/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-3-flash",
                    "max_tokens": 1024,
                    "system": "You are a helpful assistant that speaks like a pirate.",
                    "messages": [
                        {"role": "user", "content": "Tell me about the weather"}
                    ]
                }
            )
            print(f"   Status: {response.status_code}")
            result = response.json()
            if "content" in result:
                print(f"   Response: {result['content'][0]['text']}")
            else:
                print(f"   Response: {result}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 4: Messages (streaming)
        print("\n4. Testing /v1/messages (streaming)...")
        try:
            async with client.stream(
                "POST",
                f"{base_url}/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-3-flash",
                    "max_tokens": 1024,
                    "messages": [
                        {"role": "user", "content": "Count from 1 to 5"}
                    ],
                    "stream": True
                }
            ) as response:
                print(f"   Status: {response.status_code}")
                print("   Streaming response: ", end="", flush=True)
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        try:
                            import json
                            event = json.loads(data)
                            if event.get("type") == "content_block_delta":
                                text = event.get("delta", {}).get("text", "")
                                if text:
                                    print(text, end="", flush=True)
                        except:
                            pass
                print()  # New line after streaming
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_anthropic_api())
