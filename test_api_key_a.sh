#!/bin/bash

echo "Starting Gemini Gateway on port 6000 with API key 'a'..."
./venv/bin/python -u main.py --port 6000 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"
sleep 6

echo ""
echo "=========================================="
echo "Test 1: Health Check (No Auth Required)"
echo "=========================================="
curl -s http://localhost:6000/health | python3 -m json.tool

echo ""
echo "=========================================="
echo "Test 2: OpenAI Format with API Key 'a'"
echo "=========================================="
curl -s http://localhost:6000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "What is 10+10? Answer in one word."}
    ]
  }' | python3 -m json.tool

echo ""
echo "=========================================="
echo "Test 3: Anthropic Format with API Key 'a'"
echo "=========================================="
curl -s http://localhost:6000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: a" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "What is 15+5? Answer in one word."}
    ]
  }' | python3 -m json.tool

echo ""
echo "=========================================="
echo "Test 4: Wrong API Key (Should Fail)"
echo "=========================================="
curl -s http://localhost:6000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer wrong-key" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }' | python3 -m json.tool

echo ""
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo ""
echo "=========================================="
echo "✅ API Key Test Complete!"
echo "=========================================="
