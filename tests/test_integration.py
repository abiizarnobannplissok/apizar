# -*- coding: utf-8 -*-

"""
Integration tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Authentication headers for testing."""
    return {"Authorization": "Bearer gemini-secret-key-123"}


@pytest.fixture
def anthropic_headers():
    """Anthropic authentication headers for testing."""
    return {
        "x-api-key": "gemini-secret-key-123",
        "anthropic-version": "2023-06-01"
    }


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root health check."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
    
    def test_health_endpoint(self, client):
        """Test detailed health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data


class TestOpenAIEndpoints:
    """Test OpenAI-compatible endpoints."""
    
    def test_list_models_unauthorized(self, client):
        """Test models endpoint without auth."""
        response = client.get("/v1/models")
        assert response.status_code == 401
    
    def test_list_models_authorized(self, client, auth_headers):
        """Test models endpoint with auth."""
        response = client.get("/v1/models", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        assert data["data"][0]["id"] == "gemini-3-flash"
    
    def test_chat_completions_unauthorized(self, client):
        """Test chat completions without auth."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "gemini-3-flash",
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        assert response.status_code == 401
    
    def test_chat_completions_invalid_request(self, client, auth_headers):
        """Test chat completions with invalid request."""
        response = client.post(
            "/v1/chat/completions",
            headers=auth_headers,
            json={
                "model": "gemini-3-flash",
                "messages": []  # Empty messages - invalid
            }
        )
        assert response.status_code == 422
    
    def test_chat_completions_missing_model(self, client, auth_headers):
        """Test chat completions without model."""
        response = client.post(
            "/v1/chat/completions",
            headers=auth_headers,
            json={
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        assert response.status_code == 422


class TestAnthropicEndpoints:
    """Test Anthropic-compatible endpoints."""
    
    def test_messages_unauthorized(self, client):
        """Test messages endpoint without auth."""
        response = client.post(
            "/v1/messages",
            json={
                "model": "gemini-3-flash",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        assert response.status_code == 401
    
    def test_messages_invalid_request(self, client, anthropic_headers):
        """Test messages with invalid request."""
        response = client.post(
            "/v1/messages",
            headers=anthropic_headers,
            json={
                "model": "gemini-3-flash",
                "max_tokens": 1024,
                "messages": []  # Empty messages - invalid
            }
        )
        assert response.status_code == 422
    
    def test_messages_missing_max_tokens(self, client, anthropic_headers):
        """Test messages without max_tokens (should use default)."""
        response = client.post(
            "/v1/messages",
            headers=anthropic_headers,
            json={
                "model": "gemini-3-flash",
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        # Should not fail - max_tokens has default value
        assert response.status_code in [200, 500]  # 500 if Gemini API fails


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
