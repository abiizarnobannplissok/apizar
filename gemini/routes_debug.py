# -*- coding: utf-8 -*-

"""
Debug endpoint to check environment variables in Vercel deployment.
"""

import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables."""
    return {
        "PROXY_API_KEY": os.getenv("PROXY_API_KEY", "NOT_SET"),
        "PROXY_API_KEY_length": len(os.getenv("PROXY_API_KEY", "")),
        "GEMINI_API_BASE_URL": os.getenv("GEMINI_API_BASE_URL", "NOT_SET"),
        "SERVER_HOST": os.getenv("SERVER_HOST", "NOT_SET"),
        "SERVER_PORT": os.getenv("SERVER_PORT", "NOT_SET"),
        "all_env_keys": list(os.environ.keys())
    }
