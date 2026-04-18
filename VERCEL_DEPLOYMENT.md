# Vercel Deployment Guide for Gemini Gateway

This guide provides step-by-step instructions for deploying the Gemini Gateway FastAPI application to Vercel's serverless platform.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Configuration Overview](#configuration-overview)
3. [Environment Variables](#environment-variables)
4. [Deployment Steps](#deployment-steps)
5. [Vercel-Specific Limitations](#vercel-specific-limitations)
6. [Testing the Deployment](#testing-the-deployment)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Vercel account (sign up at https://vercel.com)
- Vercel CLI installed (optional but recommended): `npm install -g vercel`
- Git repository (GitHub, GitLab, or Bitbucket)
- Valid Gemini API access

## Configuration Overview

The deployment uses the following files:

### 1. `vercel.json`
Main configuration file that defines:
- Build settings using `@vercel/python`
- Route handling to direct all requests to the serverless function
- Function timeout settings (60 seconds)
- Default environment variables

### 2. `api/index.py`
Serverless function entry point that:
- Uses Mangum adapter to convert FastAPI to ASGI handler
- Imports the main FastAPI app
- Disables lifespan events (not supported in serverless)

### 3. `.vercelignore`
Excludes unnecessary files from deployment:
- Test files and scripts
- Documentation (except README and this file)
- Virtual environments
- Cache directories

### 4. `requirements.txt`
Updated to include `mangum==0.17.0` for ASGI adapter support.

## Environment Variables

You **MUST** configure these environment variables in the Vercel dashboard before deployment:

### Required Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `PROXY_API_KEY` | API key for gateway authentication | `your-secure-api-key-here` |
| `GEMINI_API_BASE_URL` | Base URL for Gemini API | `https://apis.snowping.eu.cc/api/aichat/gemini` |

### Optional Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `LOG_LEVEL` | Logging level | `INFO` |
| `REQUEST_TIMEOUT` | Request timeout in seconds | `60` |
| `SERVER_HOST` | Server host (set by Vercel) | `0.0.0.0` |
| `SERVER_PORT` | Server port (set by Vercel) | `6000` |

### Setting Environment Variables

#### Via Vercel Dashboard:
1. Go to your project in Vercel dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add each variable with its value
4. Select the environment(s): Production, Preview, Development
5. Click **Save**

#### Via Vercel CLI:
```bash
vercel env add PROXY_API_KEY
vercel env add GEMINI_API_BASE_URL
vercel env add LOG_LEVEL
vercel env add REQUEST_TIMEOUT
```

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended for first-time)

1. **Push code to Git repository**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Import project to Vercel**
   - Go to https://vercel.com/new
   - Click "Import Project"
   - Select your Git repository
   - Vercel will auto-detect the configuration

3. **Configure environment variables**
   - Before clicking "Deploy", add all required environment variables
   - See [Environment Variables](#environment-variables) section above

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (usually 1-2 minutes)
   - Vercel will provide a deployment URL

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed)
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from project directory**
   ```bash
   cd /media/abiizar/DATA/snowping/gemini_gateway
   vercel
   ```

4. **Follow the prompts**
   - Set up and deploy: Yes
   - Which scope: Select your account
   - Link to existing project: No (first time) or Yes (subsequent deploys)
   - Project name: gemini-gateway (or your preferred name)
   - Directory: ./ (current directory)

5. **Set environment variables**
   ```bash
   vercel env add PROXY_API_KEY production
   vercel env add GEMINI_API_BASE_URL production
   ```

6. **Deploy to production**
   ```bash
   vercel --prod
   ```

## Vercel-Specific Limitations

### 1. **Function Timeout**
- **Hobby Plan**: 10 seconds maximum
- **Pro Plan**: 60 seconds maximum (configured in vercel.json)
- **Enterprise Plan**: 900 seconds maximum

**Impact**: Long-running requests may timeout. The current configuration sets 60 seconds, which should be sufficient for most chat completions.

**Mitigation**: 
- Use streaming responses when possible
- Consider upgrading to Pro plan if needed
- Monitor timeout errors in Vercel logs

### 2. **Cold Starts**
- Serverless functions may experience cold starts (1-3 seconds delay)
- First request after inactivity will be slower

**Mitigation**:
- Accept this as normal serverless behavior
- Consider using Vercel's Edge Functions for faster cold starts (requires code changes)

### 3. **Streaming Responses**
- Vercel supports streaming, but with some limitations
- Response streaming works with Server-Sent Events (SSE)

**Status**: The application uses SSE for streaming, which is compatible with Vercel.

### 4. **File System**
- Serverless functions have read-only file system (except /tmp)
- No persistent storage between requests

**Impact**: Logging to files won't work. Use Vercel's logging system instead.

**Current Setup**: The app logs to stderr, which Vercel captures automatically.

### 5. **Memory Limits**
- **Hobby Plan**: 1024 MB
- **Pro Plan**: 3008 MB

**Impact**: Should be sufficient for this application.

### 6. **Request/Response Size**
- Maximum request body: 4.5 MB
- Maximum response body: 4.5 MB

**Impact**: Very large prompts or responses may fail.

### 7. **Concurrent Executions**
- Vercel automatically scales based on traffic
- No manual configuration needed

## Testing the Deployment

### 1. Health Check
Once deployed, test the health endpoint:
```bash
curl https://your-deployment-url.vercel.app/health
```

### 2. OpenAI-Compatible Endpoint
```bash
curl -X POST https://your-deployment-url.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_PROXY_API_KEY" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### 3. Anthropic-Compatible Endpoint
```bash
curl -X POST https://your-deployment-url.vercel.app/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_PROXY_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 1024
  }'
```

### 4. API Documentation
Access the interactive API docs:
```
https://your-deployment-url.vercel.app/docs
```

### 5. Check Logs
View real-time logs in Vercel dashboard:
1. Go to your project
2. Click on the deployment
3. Navigate to "Functions" tab
4. Click on "Logs"

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Ensure all dependencies are in `requirements.txt` and the deployment rebuilt.

```bash
vercel --prod --force
```

### Issue: "Function timeout" error

**Solution**: 
1. Check if you're on Hobby plan (10s limit)
2. Upgrade to Pro plan for 60s timeout
3. Optimize your Gemini API calls

### Issue: Environment variables not working

**Solution**:
1. Verify variables are set in Vercel dashboard
2. Redeploy after adding variables
3. Check variable names match exactly (case-sensitive)

### Issue: CORS errors

**Solution**: The app already has CORS middleware configured to allow all origins. If issues persist:
1. Check browser console for specific error
2. Verify the request includes proper headers
3. Check Vercel function logs for errors

### Issue: 404 Not Found

**Solution**:
1. Verify the route exists in your FastAPI app
2. Check `vercel.json` routes configuration
3. Ensure `api/index.py` is properly importing the app

### Issue: Streaming not working

**Solution**:
1. Verify client supports SSE (Server-Sent Events)
2. Check that `stream=true` is set in request
3. Monitor Vercel logs for streaming errors

## Monitoring and Maintenance

### View Deployment Logs
```bash
vercel logs your-deployment-url.vercel.app
```

### View Function Metrics
- Go to Vercel dashboard
- Select your project
- Navigate to "Analytics" tab
- View function invocations, errors, and duration

### Rollback to Previous Deployment
If something goes wrong:
1. Go to Vercel dashboard
2. Select your project
3. Click "Deployments"
4. Find a working deployment
5. Click "..." → "Promote to Production"

## Performance Optimization

### 1. Enable Edge Caching
Add caching headers for static responses (if applicable):
```python
@app.get("/v1/models")
async def list_models():
    response = JSONResponse(content=models_data)
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response
```

### 2. Monitor Cold Starts
- Check function execution time in Vercel analytics
- Consider keeping functions warm with periodic health checks

### 3. Optimize Dependencies
- Only include necessary packages in requirements.txt
- Consider using lighter alternatives if available

## Security Considerations

### 1. API Key Protection
- Never commit `.env` file to Git
- Use Vercel's environment variables for secrets
- Rotate API keys regularly

### 2. Rate Limiting
Consider adding rate limiting middleware:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### 3. HTTPS Only
Vercel automatically provides HTTPS. Ensure clients always use HTTPS URLs.

## Cost Considerations

### Vercel Pricing Tiers

**Hobby (Free)**:
- 100 GB bandwidth/month
- 100 hours serverless function execution/month
- 10s function timeout
- Good for: Testing, personal projects

**Pro ($20/month)**:
- 1 TB bandwidth/month
- 1000 hours serverless function execution/month
- 60s function timeout
- Good for: Production applications, small-medium traffic

**Enterprise (Custom)**:
- Custom limits
- 900s function timeout
- Good for: High-traffic applications

### Estimating Costs
- Average request: ~500ms execution time
- 1000 requests/day = ~8.3 hours/month
- Should fit within Hobby plan for low-medium traffic

## Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Mangum Documentation](https://mangum.io/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Vercel CLI Reference](https://vercel.com/docs/cli)

## Support

For issues specific to:
- **Vercel platform**: https://vercel.com/support
- **This application**: Create an issue in the project repository
- **Gemini API**: Contact Gemini API support

---

**Last Updated**: 2026-04-18
**Configuration Version**: 1.0
