# -*- coding: utf-8 -*-

"""
Gemini Gateway Configuration.

Centralized storage for all settings and constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================================================================================================
# Application Info
# ==================================================================================================

APP_TITLE = "Gemini Gateway"
APP_DESCRIPTION = "OpenAI and Anthropic compatible interface for Gemini 3 Flash API"
APP_VERSION = "1.0.0"

# ==================================================================================================
# Server Settings
# ==================================================================================================

DEFAULT_SERVER_HOST = "0.0.0.0"
SERVER_HOST = os.getenv("SERVER_HOST", DEFAULT_SERVER_HOST)

DEFAULT_SERVER_PORT = 6000
SERVER_PORT = int(os.getenv("SERVER_PORT", str(DEFAULT_SERVER_PORT)))

# ==================================================================================================
# Proxy Server Settings
# ==================================================================================================

# API key for proxy access (clients must pass it in Authorization header)
PROXY_API_KEY = os.getenv("PROXY_API_KEY", "a")

# ==================================================================================================
# Gemini API Settings
# ==================================================================================================

# Gemini API base URL
GEMINI_API_BASE_URL = os.getenv("GEMINI_API_BASE_URL", "https://apis.snowping.eu.cc/api/aichat/gemini")

# Default model name
DEFAULT_MODEL = "gemini-3-flash"

# ==================================================================================================
# Logging Settings
# ==================================================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==================================================================================================
# Timeout Settings
# ==================================================================================================

# HTTP request timeout (seconds)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
