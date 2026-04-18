# -*- coding: utf-8 -*-

"""
Manual test script for OpenAI-compatible API.

Run this script to test the gateway with OpenAI format.
"""

import asyncio
import httpx


async def test_openai_api():
    """Test OpenAI-compatible endpoints."""
    base_url = "http://localhost:6000"
    api_key = "gemini-secret-key-123"
    
    print("=" * 60)
    print("Testing Gemini Gateway - OpenAI API")
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
        
        # Test 2: List models
        print("\n2. Testing /v1/models...")
        try:
            response = await client.get(
                f"{base_url}/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Models: {response.json()}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 3: Chat completion (non-streaming)
        print("\n3. Testing /v1/chat/completions (non-streaming)...")
        try:
            response = await client.post(
                f"{base_url}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-3-flash",
                    "messages": [
                        {"role": "user", "content": "Say hello in 5 words"}
                    ]
                }
            )
            print(f"   Status: {response.status_code}")
            result = response.json()
            if "choices" in result:
                print(f"   Response: {result['choices'][0]['message']['content']}")
            else:
                print(f"   Response: {result}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 4: Chat completion (streaming)
        print("\n4. Testing /v1/chat/completions (streaming)...")
        try:
            async with client.stream(
                "POST",
                f"{base_url}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-3-flash",
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
                        if data == "[DONE]":
                            break
                        try:
                            import json
                            chunk = json.loads(data)
                            if "choices" in chunk and chunk["choices"]:
                                content = chunk["choices"][0]["delta"].get("content", "")
                                if content:
                                    print(content, end="", flush=True)
                        except:
                            pass
                print()  # New line after streaming
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_openai_api())
