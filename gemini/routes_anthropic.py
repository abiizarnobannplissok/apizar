# -*- coding: utf-8 -*-

"""
FastAPI routes for Anthropic-compatible API endpoints.
"""

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Security
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import APIKeyHeader
from loguru import logger

from gemini.config import PROXY_API_KEY, GEMINI_API_BASE_URL, REQUEST_TIMEOUT
from gemini.models_anthropic import AnthropicRequest
from gemini.converters_anthropic import build_gemini_params_from_anthropic
from gemini.response_anthropic import convert_gemini_to_anthropic, create_anthropic_stream_event


# --- Security scheme ---
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_anthropic_api_key(auth_header: str = Security(api_key_header)) -> bool:
    """Verify API key in x-api-key header (Anthropic style)."""
    if not auth_header or auth_header != PROXY_API_KEY:
        logger.warning("Access attempt with invalid API key.")
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return True


# --- Router ---
router = APIRouter()


@router.post("/v1/messages", dependencies=[Depends(verify_anthropic_api_key)])
async def create_message(request: Request, request_data: AnthropicRequest):
    """
    Messages endpoint - compatible with Anthropic API.
    
    Accepts requests in Anthropic format and translates them to Gemini API.
    """
    logger.info(f"Request to /v1/messages (model={request_data.model}, stream={request_data.stream})")
    
    # Build Gemini API parameters
    try:
        gemini_params = build_gemini_params_from_anthropic(request_data)
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
            messages_dict = []
            for msg in request_data.messages:
                if isinstance(msg.content, str):
                    messages_dict.append({"content": msg.content, "role": msg.role})
                else:
                    # Handle content blocks
                    content_text = " ".join(
                        block.text for block in msg.content 
                        if hasattr(block, 'text') and block.text
                    )
                    messages_dict.append({"content": content_text, "role": msg.role})
            
            if request_data.stream:
                # Streaming mode - simulate Anthropic streaming format
                async def stream_wrapper():
                    try:
                        text = gemini_response.get("result", {}).get("text", "")
                        
                        # Send message_start event
                        yield create_anthropic_stream_event("", "message_start")
                        
                        # Send content_block_start event
                        yield create_anthropic_stream_event("", "content_block_start")
                        
                        # Send content_block_delta event with text
                        yield create_anthropic_stream_event(text, "content_block_delta")
                        
                        # Send content_block_stop event
                        yield create_anthropic_stream_event("", "content_block_stop")
                        
                        # Send message_delta event
                        yield create_anthropic_stream_event("", "message_delta")
                        
                        # Send message_stop event
                        yield create_anthropic_stream_event("", "message_stop")
                        
                        logger.info("Streaming completed successfully")
                    except Exception as e:
                        logger.error(f"Streaming error: {e}")
                        raise
                
                return StreamingResponse(stream_wrapper(), media_type="text/event-stream")
            else:
                # Non-streaming mode
                anthropic_response = convert_gemini_to_anthropic(
                    gemini_response,
                    request_data.model,
                    messages_dict
                )
                
                logger.info("Non-streaming request completed successfully")
                return JSONResponse(content=anthropic_response)
    
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
