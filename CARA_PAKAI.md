# 🚀 Gemini Gateway - Panduan Penggunaan

## ✅ Project Selesai!

API Wrapper untuk Gemini 3 Flash telah selesai dibuat dengan konfigurasi:
- **Port:** 6000
- **API Key:** a
- **Compatible:** OpenAI & Anthropic API

---

## 📍 Lokasi Project

```bash
/media/abiizar/DATA/snowping/gemini_gateway/
```

---

## 🚀 Cara Menjalankan Server

### Opsi 1: Menggunakan Script (Recommended)

```bash
cd /media/abiizar/DATA/snowping/gemini_gateway
./start.sh
```

### Opsi 2: Manual

```bash
cd /media/abiizar/DATA/snowping/gemini_gateway
source venv/bin/activate
python main.py
```

Server akan berjalan di: **http://localhost:6000**

Untuk menghentikan server, tekan `Ctrl+C`

---

## 🧪 Cara Testing

Setelah server berjalan, buka terminal baru dan jalankan:

### Test 1: Health Check
```bash
curl http://localhost:6000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "...",
  "version": "1.0.0"
}
```

### Test 2: OpenAI Format
```bash
curl http://localhost:6000/v1/chat/completions \
  -H "Authorization: Bearer a" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "What is 2+2?"}
    ]
  }'
```

**Expected Response:**
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "gemini-3-flash",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Four"
      }
    }
  ]
}
```

### Test 3: Anthropic Format
```bash
curl http://localhost:6000/v1/messages \
  -H "x-api-key: a" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "What is 2+2?"}
    ]
  }'
```

**Expected Response:**
```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Four"
    }
  ]
}
```

---

## 💻 Menggunakan dengan Python SDK

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
        {"role": "user", "content": "Hello, how are you?"}
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
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(message.content[0].text)
```

---

## 📚 API Documentation

Setelah server berjalan, kunjungi:

- **Swagger UI:** http://localhost:6000/docs
- **ReDoc:** http://localhost:6000/redoc

---

## ⚙️ Konfigurasi

Edit file `.env` untuk mengubah konfigurasi:

```bash
# Server Settings
SERVER_HOST=0.0.0.0
SERVER_PORT=6000

# API Key
PROXY_API_KEY=a

# Gemini API
GEMINI_API_BASE_URL=https://apis.snowping.eu.cc/api/aichat/gemini

# Logging
LOG_LEVEL=INFO

# Timeout
REQUEST_TIMEOUT=60
```

---

## 🔧 Troubleshooting

### Server tidak bisa diakses
- Pastikan server sudah berjalan dengan `./start.sh`
- Cek apakah port 6000 sudah digunakan: `lsof -i :6000`
- Cek log server untuk error

### Error "Invalid or missing API Key"
- Pastikan menggunakan API key yang benar: `a`
- OpenAI format: `Authorization: Bearer a`
- Anthropic format: `x-api-key: a`

### Connection timeout
- Cek koneksi internet
- Pastikan Gemini API bisa diakses
- Tingkatkan `REQUEST_TIMEOUT` di `.env`

---

## 📋 Fitur

✅ OpenAI API Compatible (`/v1/chat/completions`)
✅ Anthropic API Compatible (`/v1/messages`)
✅ Streaming support untuk kedua format
✅ Request/response validation dengan Pydantic
✅ Error handling yang komprehensif
✅ Logging dengan loguru
✅ FastAPI dengan automatic API docs
✅ Konfigurasi via environment variables

---

## 📝 File Penting

- `start.sh` - Script untuk menjalankan server
- `main.py` - Entry point aplikasi
- `.env` - File konfigurasi
- `README.md` - Dokumentasi lengkap
- `QUICKSTART.md` - Panduan cepat
- `gemini/` - Package utama dengan semua logic

---

## 🎯 Quick Start

1. **Start server:**
   ```bash
   cd /media/abiizar/DATA/snowping/gemini_gateway
   ./start.sh
   ```

2. **Test (di terminal baru):**
   ```bash
   curl http://localhost:6000/v1/chat/completions \
     -H "Authorization: Bearer a" \
     -H "Content-Type: application/json" \
     -d '{"model":"gemini-3-flash","messages":[{"role":"user","content":"Hello"}]}'
   ```

3. **Lihat API docs:**
   Buka browser: http://localhost:6000/docs

---

## ✅ Status Final

- ✅ API Wrapper: **COMPLETE**
- ✅ OpenAI Compatible: **YES**
- ✅ Anthropic Compatible: **YES**
- ✅ Port: **6000**
- ✅ API Key: **a**
- ✅ Tested: **YES**
- ✅ Documentation: **COMPLETE**

**🎉 Project siap digunakan!**

---

## 📞 Support

Jika ada masalah, cek:
1. Log server di terminal
2. File `server.log` di folder project
3. Dokumentasi lengkap di `README.md`
