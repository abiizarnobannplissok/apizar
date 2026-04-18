#!/bin/bash

# Gemini Gateway Startup Script

cd /media/abiizar/DATA/snowping/gemini_gateway

echo "=========================================="
echo "Starting Gemini Gateway"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  Port: 6000"
echo "  API Key: a"
echo ""
echo "Endpoints:"
echo "  Health: http://localhost:6000/health"
echo "  OpenAI: http://localhost:6000/v1/chat/completions"
echo "  Anthropic: http://localhost:6000/v1/messages"
echo "  API Docs: http://localhost:6000/docs"
echo ""
echo "=========================================="
echo ""

# Activate virtual environment and start server
source venv/bin/activate
python main.py
