#!/bin/bash

echo "Starting Gemini Gateway on port 6000..."
./venv/bin/python main.py > /tmp/gemini_server_6000.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to start
sleep 5

echo ""
echo "=========================================="
echo "Testing Health Check on Port 6000"
echo "=========================================="
curl -s http://localhost:6000/health | python3 -m json.tool

echo ""
echo "=========================================="
echo "Testing OpenAI Format on Port 6000"
echo "=========================================="
curl -s http://localhost:6000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "Say hello"}
    ]
  }' | python3 -m json.tool

echo ""
echo "Stopping server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo ""
echo "=========================================="
echo "✅ Port 6000 Test Complete!"
echo "=========================================="
