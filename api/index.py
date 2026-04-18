# -*- coding: utf-8 -*-

"""
Vercel Serverless Function Entry Point for Gemini Gateway.

This module adapts the FastAPI application to work with Vercel's serverless architecture.
"""

import sys
import os

# Add parent directory to path to import the main app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from main import app

# Create the Mangum handler for Vercel
handler = Mangum(app, lifespan="off")
