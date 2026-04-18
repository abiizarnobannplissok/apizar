#!/bin/bash

echo "Starting Gemini Gateway on port 6000..."
./venv/bin/python main.py > /tmp/gemini_final.log 2>&1 &
SERVER_PID=$!
sleep 5

echo ""
echo "=========================================="
echo "Test 1: Health Check"
echo "=========================================="
curl -s http://localhost:6000/health | python3 -m json.tool

echo ""
echo "=========================================="
echo "Test 2: OpenAI - List Models"
echo "=========================================="
curl -s http://localhost:6000/v1/models \
  -H "Authorization: Bearer a" | python3 -m json.tool

echo ""
echo "=========================================="
echo "Test 3: OpenAI - Chat Completion"
echo "=========================================="
curl -s http://localhost:6000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "What is 5+5? Answer in one word."}
    ]
  }' | python3 -m json.tool

echo ""
echo "=========================================="
echo "Test 4: Anthropic - Messages"
echo "=========================================="
curl -s http://localhost:6000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: a" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "What is 7+3? Answer in one word."}
    ]
  }' | python3 -m json.tool

echo ""
echo "Stopping server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo ""
echo "=========================================="
echo "✅ All Tests on Port 6000 Complete!"
echo "=========================================="
