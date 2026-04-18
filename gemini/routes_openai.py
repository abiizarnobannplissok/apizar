# -*- coding: utf-8 -*-

"""
FastAPI routes for OpenAI-compatible API endpoints.
"""

import httpx
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import APIKeyHeader
from loguru import logger

from gemini.config import PROXY_API_KEY, APP_VERSION, GEMINI_API_BASE_URL, REQUEST_TIMEOUT, DEFAULT_MODEL
from gemini.models_openai import ModelList, OpenAIModel, ChatCompletionRequest
from gemini.converters_openai import build_gemini_params
from gemini.response_openai import convert_gemini_to_openai, create_openai_stream_chunk


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


@router.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Gemini Gateway is running",
        "version": APP_VERSION
    }


@router.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": APP_VERSION
    }


@router.get("/v1/models", response_model=ModelList, dependencies=[Depends(verify_api_key)])
async def get_models():
    """Return list of available models."""
    logger.info("Request to /v1/models")
    
    models = [
        OpenAIModel(
            id=DEFAULT_MODEL,
            owned_by="google",
            description="Gemini 3 Flash model via Snowping API"
        )
    ]
    
    return ModelList(data=models)


@router.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
async def chat_completions(request_data: ChatCompletionRequest):
    """
    Chat completions endpoint - compatible with OpenAI API.
    
    Accepts requests in OpenAI format and translates them to Gemini API.
    """
    logger.info(f"Request to /v1/chat/completions (model={request_data.model}, stream={request_data.stream})")
    
    # Build Gemini API parameters
    try:
        gemini_params = build_gemini_params(request_data)
    except Exception as e:
        logger.error(f"Failed to build Gemini params: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    
    # Make request to Gemini API
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            logger.debug(f"Calling Gemini API: {GEMINI_API_BASE_URL}")
            logger.debug(f"Params: {gemini_params}")
            
            response = await client.get(GEMINI_API_BASE_URL, params=gemini_params)
            
            if response.status_code != 200:
                error_text = response.text
                logger.error(f"Gemini API error: {response.status_code} - {error_text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Gemini API error: {error_text}"
                )
            
            gemini_response = response.json()
            logger.debug(f"Gemini response: {gemini_response}")
            
            # Check if response is successful
            if gemini_response.get("status") != 200:
                raise HTTPException(
                    status_code=500,
                    detail="Gemini API returned error status"
                )
            
            # Convert messages for token estimation
            messages_dict = [{"content": msg.content, "role": msg.role} for msg in request_data.messages]
            
            if request_data.stream:
                # Streaming mode - simulate streaming by sending the full response
                async def stream_wrapper():
                    try:
                        text = gemini_response.get("result", {}).get("text", "")
                        
                        # Send content chunk
                        yield create_openai_stream_chunk(text, request_data.model, is_final=False)
                        
                        # Send final chunk
                        yield create_openai_stream_chunk("", request_data.model, is_final=True)
                        
                        # Send [DONE]
                        yield "data: [DONE]\n\n"
                        
                        logger.info("Streaming completed successfully")
                    except Exception as e:
                        logger.error(f"Streaming error: {e}")
                        raise
                
                return StreamingResponse(stream_wrapper(), media_type="text/event-stream")
            else:
                # Non-streaming mode
                openai_response = convert_gemini_to_openai(
                    gemini_response,
                    request_data.model,
                    messages_dict
                )
                
                logger.info("Non-streaming request completed successfully")
                return JSONResponse(content=openai_response)
    
    except httpx.TimeoutException:
        logger.error("Request to Gemini API timed out")
        raise HTTPException(status_code=504, detail="Request timed out")
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(status_code=502, detail=f"Failed to connect to Gemini API: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Internal error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
