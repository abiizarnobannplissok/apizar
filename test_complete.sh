#!/bin/bash

echo "Starting Gemini Gateway on port 9000..."
./venv/bin/python main.py --port 9000 > /tmp/gemini_server.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to start
sleep 5

echo ""
echo "=========================================="
echo "Testing OpenAI Format"
echo "=========================================="
curl -s http://localhost:9000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is 2+2? Answer in one word."}
    ]
  }' | python3 -m json.tool

echo ""
echo "=========================================="
echo "Testing Anthropic Format"
echo "=========================================="
curl -s http://localhost:9000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: a" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "What is 3+3? Answer in one word."}
    ]
  }' | python3 -m json.tool

echo ""
echo "Stopping server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo ""
echo "=========================================="
echo "Test Complete!"
echo "=========================================="
