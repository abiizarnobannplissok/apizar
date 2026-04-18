# Quick Start Guide - Gemini Gateway

## Installation & Setup

1. **Navigate to the project directory:**
```bash
cd /media/abiizar/DATA/snowping/gemini_gateway
```

2. **Activate virtual environment:**
```bash
source venv/bin/activate
```

3. **Configure your API key (optional):**
```bash
# Edit .env file to change the default API key
nano .env
```

## Running the Server

**Start the server:**
```bash
python main.py
```

Or on a custom port:
```bash
python main.py --port 9000
```

The server will start at `http://localhost:6000` (or your custom port).

## Quick Tests

Once the server is running, open a new terminal and run these tests:

### Test 1: Health Check
```bash
curl http://localhost:6000/health
```

### Test 2: OpenAI Format - Chat Completion
```bash
curl http://localhost:6000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is 2+2?"}
    ]
  }'
```

### Test 3: Anthropic Format - Messages
```bash
curl http://localhost:6000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: a" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "What is 2+2?"}
    ]
  }'
```

## Using with Python SDKs

### OpenAI SDK
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:6000/v1",
    api_key="a"
)

response = client.chat.completions.create(
    model="gemini-3-flash",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Anthropic SDK
```python
from anthropic import Anthropic

client = Anthropic(
    base_url="http://localhost:6000",
    api_key="a"
)

message = client.messages.create(
    model="gemini-3-flash",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(message.content[0].text)
```

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:6000/docs
- **ReDoc:** http://localhost:6000/redoc

## Project Structure

```
gemini_gateway/
├── gemini/                      # Main package
│   ├── __init__.py
│   ├── config.py               # Configuration settings
│   ├── models_openai.py        # OpenAI Pydantic models
│   ├── models_anthropic.py     # Anthropic Pydantic models
│   ├── converters_openai.py    # OpenAI → Gemini converter
│   ├── converters_anthropic.py # Anthropic → Gemini converter
│   ├── response_openai.py      # Gemini → OpenAI converter
│   ├── response_anthropic.py   # Gemini → Anthropic converter
│   ├── routes_openai.py        # OpenAI API endpoints
│   └── routes_anthropic.py     # Anthropic API endpoints
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
├── .env                        # Configuration file
├── .env.example               # Example configuration
├── README.md                  # Full documentation
├── test_manual.sh             # Manual test script
└── venv/                      # Virtual environment
```

## Features

✅ OpenAI API compatible (`/v1/chat/completions`)
✅ Anthropic API compatible (`/v1/messages`)
✅ Streaming support for both formats
✅ Easy configuration via .env file
✅ Full request/response validation
✅ Comprehensive error handling
✅ FastAPI with automatic API docs

## Troubleshooting

**Port already in use:**
```bash
python main.py --port 9000
```

**Connection errors:**
- Check if Gemini API is accessible
- Verify your internet connection
- Check firewall settings

**Authentication errors:**
- Verify API key matches in .env and client
- OpenAI format uses: `Authorization: Bearer <key>`
- Anthropic format uses: `x-api-key: <key>`
