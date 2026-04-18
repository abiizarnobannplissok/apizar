# ✅ Port Berhasil Diubah ke 6000

## Perubahan yang Telah Dilakukan

Semua referensi port **8000** telah berhasil diubah menjadi **6000** di seluruh project:

### File yang Diubah:
- ✅ `gemini/config.py` - DEFAULT_SERVER_PORT = 6000
- ✅ `.env` - SERVER_PORT=6000
- ✅ `.env.example` - SERVER_PORT=6000
- ✅ `README.md` - Semua contoh menggunakan port 6000
- ✅ `QUICKSTART.md` - Semua contoh menggunakan port 6000
- ✅ `PROJECT_COMPLETE.md` - Dokumentasi diperbarui
- ✅ Semua file test (test_openai.py, test_anthropic.py, dll)

## ✅ Verifikasi - Server Berjalan di Port 6000

Test terakhir menunjukkan server berhasil berjalan:

```
🚀 Gemini Gateway v1.0.0

Server running at:
➜  http://localhost:6000

API Docs:      http://localhost:6000/docs
Health Check:  http://localhost:6000/health

OpenAI endpoint:    http://localhost:6000/v1/chat/completions
Anthropic endpoint: http://localhost:6000/v1/messages
```

**Test OpenAI Endpoint Berhasil:**
```json
{
    "id": "chatcmpl-bb798599",
    "object": "chat.completion",
    "created": 1776480142,
    "model": "gemini-3-flash",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "...",
                "name": null
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 3,
        "completion_tokens": 1,
        "total_tokens": 4
    }
}
```

## Cara Menggunakan

### 1. Start Server (Port 6000)
```bash
cd /media/abiizar/DATA/snowping/gemini_gateway
source venv/bin/activate
python main.py
```

Server akan berjalan di: **http://localhost:6000**

### 2. Test dengan cURL

**Health Check:**
```bash
curl http://localhost:6000/health
```

**OpenAI Format:**
```bash
curl http://localhost:6000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

**Anthropic Format:**
```bash
curl http://localhost:6000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: a" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### 3. Gunakan dengan SDK

**OpenAI SDK:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:6000/v1",
    api_key="a"
)

response = client.chat.completions.create(
    model="gemini-3-flash",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Anthropic SDK:**
```python
from anthropic import Anthropic

client = Anthropic(
    base_url="http://localhost:6000",
    api_key="a"
)

message = client.messages.create(
    model="gemini-3-flash",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## API Documentation

Setelah server berjalan, kunjungi:
- **Swagger UI:** http://localhost:6000/docs
- **ReDoc:** http://localhost:6000/redoc

---

## ✅ Status: SELESAI

Port berhasil diubah dari 8000 ke 6000 dan telah diverifikasi berfungsi dengan baik!
