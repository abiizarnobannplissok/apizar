# Vercel Environment Variables - Quick Reference

## Required Variables (Must Set Before Deployment)

```bash
# Copy these commands and replace with your actual values

# Required: API key for gateway authentication
vercel env add PROXY_API_KEY
# Enter value: your-secure-api-key-here

# Required: Gemini API base URL
vercel env add GEMINI_API_BASE_URL
# Enter value: https://apis.snowping.eu.cc/api/aichat/gemini
```

## Optional Variables (Have Defaults)

```bash
# Optional: Logging level (default: INFO)
vercel env add LOG_LEVEL
# Enter value: INFO

# Optional: Request timeout in seconds (default: 60)
vercel env add REQUEST_TIMEOUT
# Enter value: 60
```

## Setting Variables via Dashboard

1. Go to: https://vercel.com/dashboard
2. Select your project
3. Navigate to: **Settings** → **Environment Variables**
4. Add each variable:
   - **Key**: `PROXY_API_KEY`
   - **Value**: `your-secure-api-key-here`
   - **Environments**: Check all (Production, Preview, Development)
   - Click **Save**

5. Repeat for `GEMINI_API_BASE_URL` and optional variables

## Verification

After setting variables, verify they're configured:

```bash
vercel env ls
```

## Security Notes

- Never commit `.env` file to Git
- Use strong, random API keys
- Rotate keys regularly
- Use different keys for Production vs Preview environments

## Testing After Deployment

```bash
# Replace YOUR_DEPLOYMENT_URL and YOUR_API_KEY
curl https://YOUR_DEPLOYMENT_URL.vercel.app/health

curl -X POST https://YOUR_DEPLOYMENT_URL.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"model":"gemini-3-flash","messages":[{"role":"user","content":"Hello"}]}'
```
