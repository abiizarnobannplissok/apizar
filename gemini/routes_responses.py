# -*- coding: utf-8 -*-

"""
FastAPI routes for /v1/responses endpoint.

This endpoint is used by OpenCode for response handling.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from loguru import logger

from gemini.config import PROXY_API_KEY, APP_VERSION


# --- Security scheme ---
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def verify_api_key(auth_header: str = Security(api_key_header)) -> bool:
    """Verify API key in Authorization header."""
    if not auth_header or auth_header != f"Bearer {PROXY_API_KEY}":
        logger.warning("Access attempt with invalid API key.")
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return True


# --- Router ---
router = APIRouter()


@router.get("/v1/responses", dependencies=[Depends(verify_api_key)])
async def get_responses():
    """
    Responses endpoint - used by OpenCode for response handling.
    
    Returns an empty list as this is a compatibility endpoint.
    """
    logger.info("Request to /v1/responses")
    
    return JSONResponse(content={
        "object": "list",
        "data": [],
        "has_more": False
    })


@router.post("/v1/responses", dependencies=[Depends(verify_api_key)])
async def create_response():
    """
    Create response endpoint - used by OpenCode for response handling.
    
    Returns success response for compatibility.
    """
    logger.info("POST request to /v1/responses")
    
    return JSONResponse(content={
        "id": f"resp_{int(datetime.now(timezone.utc).timestamp())}",
        "object": "response",
        "created": int(datetime.now(timezone.utc).timestamp()),
        "status": "completed"
    })
