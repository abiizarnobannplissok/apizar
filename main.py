# -*- coding: utf-8 -*-

"""
Gemini Gateway - OpenAI and Anthropic compatible interface for Gemini 3 Flash API.

Application entry point. Creates FastAPI app and connects routes.
"""

import sys
import argparse
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from gemini.config import (
    APP_TITLE,
    APP_DESCRIPTION,
    APP_VERSION,
    LOG_LEVEL,
    SERVER_HOST,
    SERVER_PORT,
    DEFAULT_SERVER_HOST,
    DEFAULT_SERVER_PORT,
)
from gemini.routes_openai import router as openai_router
from gemini.routes_anthropic import router as anthropic_router
from gemini.routes_debug import router as debug_router


# --- Loguru Configuration ---
logger.remove()
logger.add(
    sys.stderr,
    level=LOG_LEVEL,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)


# --- Lifespan Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the application lifecycle."""
    logger.info("Starting Gemini Gateway...")
    yield
    logger.info("Shutting down Gemini Gateway...")


# --- FastAPI Application ---
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan
)


# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Route Registration ---
# OpenAI-compatible API: /v1/models, /v1/chat/completions
app.include_router(openai_router)

# Anthropic-compatible API: /v1/messages
app.include_router(anthropic_router)

# Debug endpoints
app.include_router(debug_router)


def parse_cli_args() -> argparse.Namespace:
    """Parse command-line arguments for server configuration."""
    parser = argparse.ArgumentParser(
        description=f"{APP_TITLE} - {APP_DESCRIPTION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-H", "--host",
        type=str,
        default=None,
        metavar="HOST",
        help=f"Server host address (default: {DEFAULT_SERVER_HOST})"
    )
    
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=None,
        metavar="PORT",
        help=f"Server port (default: {DEFAULT_SERVER_PORT})"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}"
    )
    
    return parser.parse_args()


def resolve_server_config(args: argparse.Namespace) -> tuple[str, int]:
    """Resolve final server configuration using priority hierarchy."""
    final_host = args.host if args.host is not None else SERVER_HOST
    final_port = args.port if args.port is not None else SERVER_PORT
    
    logger.debug(f"Host: {final_host}")
    logger.debug(f"Port: {final_port}")
    
    return final_host, final_port


def print_startup_banner(host: str, port: int) -> None:
    """Print a startup banner with server information."""
    display_host = "localhost" if host == "0.0.0.0" else host
    url = f"http://{display_host}:{port}"
    
    print()
    print(f"  🚀 {APP_TITLE} v{APP_VERSION}")
    print()
    print(f"  Server running at:")
    print(f"  ➜  {url}")
    print()
    print(f"  API Docs:      {url}/docs")
    print(f"  Health Check:  {url}/health")
    print()
    print(f"  OpenAI endpoint:    {url}/v1/chat/completions")
    print(f"  Anthropic endpoint: {url}/v1/messages")
    print()


# --- Entry Point ---
if __name__ == "__main__":
    import uvicorn
    
    # Parse CLI arguments
    args = parse_cli_args()
    
    # Resolve final configuration
    final_host, final_port = resolve_server_config(args)
    
    # Print startup banner
    print_startup_banner(final_host, final_port)
    
    logger.info(f"Starting Uvicorn server on {final_host}:{final_port}...")
    
    # Start server
    uvicorn.run(
        "main:app",
        host=final_host,
        port=final_port,
        log_level=LOG_LEVEL.lower(),
    )
