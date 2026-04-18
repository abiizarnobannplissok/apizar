# -*- coding: utf-8 -*-

"""
HTTP client for Gemini API with retry logic.
"""

import asyncio
from typing import Optional
import httpx
from loguru import logger

from gemini.config import (
    GEMINI_API_BASE_URL,
    MAX_RETRIES,
    BASE_RETRY_DELAY,
    CONNECT_TIMEOUT,
    READ_TIMEOUT
)


class GeminiHttpClient:
    """
    HTTP client for Gemini API with automatic retry logic.
    """
    
    def __init__(self, base_url: str = GEMINI_API_BASE_URL):
        """
        Initialize HTTP client.
        
        Args:
            base_url: Base URL for Gemini API
        """
        self.base_url = base_url
        self.timeout = httpx.Timeout(
            connect=CONNECT_TIMEOUT,
            read=READ_TIMEOUT,
            write=30.0,
            pool=30.0
        )
    
    async def request_with_retry(
        self,
        params: dict,
        stream: bool = False
    ) -> httpx.Response:
        """
        Make HTTP request with automatic retry on failures.
        
        Args:
            params: Query parameters for the request
            stream: Whether to stream the response
        
        Returns:
            HTTP response
        
        Raises:
            httpx.HTTPError: If all retry attempts fail
        """
        last_error = None
        
        for attempt in range(MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    logger.debug(
                        f"Gemini API request (attempt {attempt + 1}/{MAX_RETRIES}): "
                        f"q_length={len(params.get('q', ''))}, "
                        f"inst_length={len(params.get('inst', ''))}"
                    )
                    
                    response = await client.get(
                        self.base_url,
                        params=params,
                        follow_redirects=True
                    )
                    
                    # Check for successful response
                    if response.status_code == 200:
                        logger.debug(f"Gemini API request successful")
                        return response
                    
                    # Log error response
                    logger.warning(
                        f"Gemini API returned {response.status_code}: "
                        f"{response.text[:200]}"
                    )
                    
                    # Retry on server errors (5xx) and rate limits (429)
                    if response.status_code >= 500 or response.status_code == 429:
                        last_error = Exception(
                            f"HTTP {response.status_code}: {response.text[:200]}"
                        )
                        
                        if attempt < MAX_RETRIES - 1:
                            delay = BASE_RETRY_DELAY * (2 ** attempt)
                            logger.info(
                                f"Retrying after {delay}s "
                                f"(attempt {attempt + 1}/{MAX_RETRIES})"
                            )
                            await asyncio.sleep(delay)
                            continue
                    
                    # Don't retry on client errors (4xx except 429)
                    return response
            
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_error = e
                logger.warning(f"Connection error: {e}")
                
                if attempt < MAX_RETRIES - 1:
                    delay = BASE_RETRY_DELAY * (2 ** attempt)
                    logger.info(
                        f"Retrying after {delay}s "
                        f"(attempt {attempt + 1}/{MAX_RETRIES})"
                    )
                    await asyncio.sleep(delay)
                    continue
                
                raise
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)
                raise
        
        # All retries exhausted
        if last_error:
            raise last_error
        
        raise Exception("All retry attempts failed")
