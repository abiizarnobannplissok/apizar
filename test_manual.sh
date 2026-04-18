#!/bin/bash

# Simple test script for Gemini Gateway
# Start server manually first: ./venv/bin/python main.py --port 9000

PORT=9000
BASE_URL="http://localhost:${PORT}"
API_KEY="a"

echo "============================================================"
echo "Gemini Gateway Manual Test Script"
echo "============================================================"
echo ""
echo "Make sure the server is running on port ${PORT}"
echo "Start with: ./venv/bin/python main.py --port ${PORT}"
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "============================================================"
echo "TEST 1: Health Check"
echo "============================================================"
curl -s "${BASE_URL}/health" | python3 -m json.tool
echo ""

echo ""
echo "============================================================"
echo "TEST 2: OpenAI - List Models"
echo "============================================================"
curl -s "${BASE_URL}/v1/models" \
  -H "Authorization: Bearer ${API_KEY}" | python3 -m json.tool
echo ""

echo ""
echo "============================================================"
echo "TEST 3: OpenAI - Chat Completion (Non-Streaming)"
echo "============================================================"
curl -s "${BASE_URL}/v1/chat/completions" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is 2+2? Answer in one word."}
    ],
    "stream": false
  }' | python3 -m json.tool
echo ""

echo ""
echo "============================================================"
echo "TEST 4: OpenAI - Chat Completion (Streaming)"
echo "============================================================"
curl -s "${BASE_URL}/v1/chat/completions" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "Say hello"}
    ],
    "stream": true
  }'
echo ""
echo ""

echo ""
echo "============================================================"
echo "TEST 5: Anthropic - Messages (Non-Streaming)"
echo "============================================================"
curl -s "${BASE_URL}/v1/messages" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "What is 3+3? Answer in one word."}
    ]
  }' | python3 -m json.tool
echo ""

echo ""
echo "============================================================"
echo "TEST 6: Anthropic - Messages (Streaming)"
echo "============================================================"
curl -s "${BASE_URL}/v1/messages" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Say hello"}
    ],
    "stream": true
  }'
echo ""
echo ""

echo "============================================================"
echo "Tests completed!"
echo "============================================================"
