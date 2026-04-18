#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Verification script for Gemini Gateway.

This script verifies that the gateway is properly configured and working.
"""

import sys
import os
import asyncio
import httpx
from pathlib import Path


class Colors:
    """ANSI color codes."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_header(text: str):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"  {text}")


def check_python_version():
    """Check Python version."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print_header("Checking Dependencies")
    
    required = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "httpx",
        "python-dotenv",
        "loguru"
    ]
    
    all_installed = True
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package} (not installed)")
            all_installed = False
    
    if not all_installed:
        print_warning("\nInstall missing dependencies with:")
        print_info("pip install -r requirements.txt")
    
    return all_installed


def check_configuration():
    """Check configuration files."""
    print_header("Checking Configuration")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print_success(".env file exists")
        
        # Check for required variables
        from dotenv import dotenv_values
        config = dotenv_values(".env")
        
        if "PROXY_API_KEY" in config:
            if config["PROXY_API_KEY"] == "gemini-secret-key-123":
                print_warning("PROXY_API_KEY is using default value (change it!)")
            else:
                print_success("PROXY_API_KEY is configured")
        else:
            print_error("PROXY_API_KEY not found in .env")
        
        if "GEMINI_API_BASE_URL" in config:
            print_success(f"GEMINI_API_BASE_URL: {config['GEMINI_API_BASE_URL']}")
        else:
            print_warning("GEMINI_API_BASE_URL not set (using default)")
        
        return True
    else:
        print_error(".env file not found")
        print_warning("Create .env file from template:")
        print_info("cp .env.example .env")
        return False


async def check_server_running():
    """Check if server is running."""
    print_header("Checking Server Status")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:6000/health")
            if response.status_code == 200:
                data = response.json()
                print_success(f"Server is running (version {data.get('version', 'unknown')})")
                return True
            else:
                print_error(f"Server returned status {response.status_code}")
                return False
    except httpx.ConnectError:
        print_error("Server is not running")
        print_warning("Start the server with:")
        print_info("python main.py")
        return False
    except Exception as e:
        print_error(f"Error checking server: {e}")
        return False


async def test_api_endpoints():
    """Test API endpoints."""
    print_header("Testing API Endpoints")
    
    from dotenv import dotenv_values
    config = dotenv_values(".env")
    api_key = config.get("PROXY_API_KEY", "gemini-secret-key-123")
    
    base_url = "http://localhost:6000"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test OpenAI models endpoint
            print_info("Testing /v1/models...")
            response = await client.get(
                f"{base_url}/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            if response.status_code == 200:
                print_success("OpenAI /v1/models endpoint working")
            else:
                print_error(f"OpenAI /v1/models failed: {response.status_code}")
            
            # Test OpenAI chat completions
            print_info("Testing /v1/chat/completions...")
            response = await client.post(
                f"{base_url}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-3-flash",
                    "messages": [{"role": "user", "content": "Say 'test'"}]
                }
            )
            if response.status_code == 200:
                print_success("OpenAI /v1/chat/completions endpoint working")
            else:
                print_error(f"OpenAI /v1/chat/completions failed: {response.status_code}")
                print_info(f"Response: {response.text[:200]}")
            
            # Test Anthropic messages endpoint
            print_info("Testing /v1/messages...")
            response = await client.post(
                f"{base_url}/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-3-flash",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": "Say 'test'"}]
                }
            )
            if response.status_code == 200:
                print_success("Anthropic /v1/messages endpoint working")
            else:
                print_error(f"Anthropic /v1/messages failed: {response.status_code}")
                print_info(f"Response: {response.text[:200]}")
            
            return True
    except Exception as e:
        print_error(f"Error testing endpoints: {e}")
        return False


async def main():
    """Main verification function."""
    print(f"\n{Colors.BOLD}Gemini Gateway Verification{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")
    
    results = []
    
    # Run checks
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Configuration", check_configuration()))
    results.append(("Server Status", await check_server_running()))
    
    # Only test endpoints if server is running
    if results[-1][1]:
        results.append(("API Endpoints", await test_api_endpoints()))
    
    # Print summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check, result in results:
        if result:
            print_success(f"{check}: PASSED")
        else:
            print_error(f"{check}: FAILED")
    
    print(f"\n{Colors.BOLD}Result: {passed}/{total} checks passed{Colors.RESET}\n")
    
    if passed == total:
        print_success("All checks passed! Gateway is ready to use.")
        return 0
    else:
        print_error("Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
