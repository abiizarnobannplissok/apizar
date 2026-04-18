# Gemini Gateway

OpenAI and Anthropic compatible interface for Gemini 3 Flash API.

This gateway allows you to use the Gemini 3 Flash API (via Snowping) with any client that supports OpenAI or Anthropic API formats.

## Features

- ✅ **OpenAI API Compatible** - Works with OpenAI SDK and any OpenAI-compatible clients
- ✅ **Anthropic API Compatible** - Works with Anthropic SDK and Claude-compatible clients
- ✅ **Streaming Support** - Supports both streaming and non-streaming responses
- ✅ **Easy Setup** - Simple configuration via environment variables
- ✅ **FastAPI** - Built on modern, fast FastAPI framework
- ✅ **Type Safety** - Full Pydantic validation for requests and responses

## Installation

1. Clone or download this repository:
```bash
cd gemini_gateway
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create configuration file:
```bash
cp .env.example .env
```

4. Edit `.env` and set your API key:
```bash
PROXY_API_KEY=your-secret-key-here
```

## Usage

### Start the Server

```bash
python main.py
```

Or with custom host/port:
```bash
python main.py --host 127.0.0.1 --port 9000
```

The server will start at `http://localhost:6000` by default.

### Using with OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:6000/v1",
    api_key="your-secret-key-here"
)

response = client.chat.completions.create(
    model="gemini-3-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2+2?"}
    ]
)

print(response.choices[0].message.content)
```

### Using with Anthropic SDK

```python
from anthropic import Anthropic

client = Anthropic(
    base_url="http://localhost:6000",
    api_key="your-secret-key-here"
)

message = client.messages.create(
    model="gemini-3-flash",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is 2+2?"}
    ]
)

print(message.content[0].text)
```

### Using with cURL

**OpenAI Format:**
```bash
curl http://localhost:6000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-key-here" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

**Anthropic Format:**
```bash
curl http://localhost:6000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-key-here" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

## API Endpoints

### OpenAI Compatible

- `GET /v1/models` - List available models
- `POST /v1/chat/completions` - Create chat completion

### Anthropic Compatible

- `POST /v1/messages` - Create message

### Health Check

- `GET /` - Basic health check
- `GET /health` - Detailed health check

## Configuration

All configuration is done via environment variables in `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_HOST` | Server host address | `0.0.0.0` |
| `SERVER_PORT` | Server port | `6000` |
| `PROXY_API_KEY` | API key for authentication | `a` |
| `GEMINI_API_BASE_URL` | Gemini API endpoint | `https://apis.snowping.eu.cc/api/aichat/gemini` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `REQUEST_TIMEOUT` | HTTP request timeout (seconds) | `60` |

## Streaming

Both OpenAI and Anthropic streaming formats are supported:

**OpenAI Streaming:**
```python
stream = client.chat.completions.create(
    model="gemini-3-flash",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

**Anthropic Streaming:**
```python
with client.messages.stream(
    model="gemini-3-flash",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="")
```

## Architecture

The gateway translates between different API formats:

```
OpenAI/Anthropic Request → Converter → Gemini API → Response Converter → OpenAI/Anthropic Response
```

### Project Structure

```
gemini_gateway/
├── gemini/
│   ├── __init__.py
│   ├── config.py                    # Configuration
│   ├── models_openai.py             # OpenAI Pydantic models
│   ├── models_anthropic.py          # Anthropic Pydantic models
│   ├── converters_openai.py         # OpenAI → Gemini converter
│   ├── converters_anthropic.py      # Anthropic → Gemini converter
│   ├── response_openai.py           # Gemini → OpenAI converter
│   ├── response_anthropic.py        # Gemini → Anthropic converter
│   ├── routes_openai.py             # OpenAI API routes
│   └── routes_anthropic.py          # Anthropic API routes
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Example configuration
└── README.md                        # This file
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 6000
```

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:6000/docs
- ReDoc: http://localhost:6000/redoc

## Troubleshooting

### Connection Errors

If you get connection errors to the Gemini API:
- Check your internet connection
- Verify the `GEMINI_API_BASE_URL` is correct
- Check if the Gemini API is accessible from your network

### Authentication Errors

If you get 401 errors:
- Verify your `PROXY_API_KEY` matches in both `.env` and your client
- For OpenAI format, use `Authorization: Bearer <key>`
- For Anthropic format, use `x-api-key: <key>`

### Timeout Errors

If requests timeout:
- Increase `REQUEST_TIMEOUT` in `.env`
- Check if the Gemini API is responding slowly

## License

This project is open source and available under the MIT License.

## Credits

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Gemini API provided by [Snowping](https://apis.snowping.eu.cc/)
- Inspired by [kiro-gateway](https://github.com/jwadow/kiro-gateway)

## Support

For issues, questions, or contributions, please open an issue on the project repository.
