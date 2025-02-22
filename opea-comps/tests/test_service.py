import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from comps.embedding import app as embedding_app
from comps.llm import app as llm_app
from comps.mega import app as mega_app

# Create test clients
embedding_client = TestClient(embedding_app)
llm_client = TestClient(llm_app)
mega_client = TestClient(mega_app)

# Mock responses
MOCK_EMBEDDING_RESPONSE = {
    "model": "text-embedding-ada-002",
    "embedding": [0.1, 0.2, 0.3],
    "message": "Hello, world!"
}

MOCK_LLM_RESPONSE = {
    "model": "test-model",
    "choices": [{
        "message": {
            "role": "assistant",
            "content": "This is a test response"
        }
    }]
}

def test_embedding_service():
    # Test root endpoint
    response = embedding_client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Embedding Service"

    # Test health check
    response = embedding_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    # Test embedding creation
    response = embedding_client.post(
        "/v1/embeddings",
        json={"model": "test-model", "messages": "Hello, world!"}
    )
    assert response.status_code == 200
    assert "embedding" in response.json()
    assert len(response.json()["embedding"]) == 3  # Our mock returns 3 numbers

def test_llm_service():
    # Test root endpoint
    response = llm_client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "LLM Service"

    # Test health check
    response = llm_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    # Test chat completion
    response = llm_client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "model": "test-model"
        }
    )
    assert response.status_code == 200
    assert "choices" in response.json()
    assert response.json()["choices"][0]["message"]["role"] == "assistant"

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):  # Sync method for TestClient
        return self._json_data

    async def __call__(self, *args, **kwargs):  # Make the mock callable
        return self

@pytest.mark.asyncio
@patch('httpx.AsyncClient.get')
async def test_mega_service(mock_get):
    # Create mock responses for both health checks
    mock_response1 = MockResponse({"status": "healthy"})
    mock_response2 = MockResponse({"status": "healthy"})
    
    # Set up mock to return responses in sequence
    mock_get.side_effect = [mock_response1, mock_response2]
    
    # Make responses callable
    mock_response1.__call__ = AsyncMock(return_value=mock_response1)
    mock_response2.__call__ = AsyncMock(return_value=mock_response2)
    
    # Test root endpoint
    response = mega_client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Mega Service"

    # Test health check
    response = mega_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
@patch('httpx.AsyncClient.post')
async def test_mega_service_example(mock_post):
    # Create mock responses
    embedding_response = MockResponse(MOCK_EMBEDDING_RESPONSE)
    llm_response = MockResponse(MOCK_LLM_RESPONSE)
    
    # Set up mock to return responses in sequence
    responses = [embedding_response, llm_response]
    mock_post.side_effect = responses
    for resp in responses:
        resp.__call__ = AsyncMock(return_value=resp)  # Make each response callable
    
    response = mega_client.post(
        "/v1/example-service",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "model": "test-model"
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "embedding_result" in result
    assert "llm_result" in result

def test_service_creation():
    from comps.service import MicroService, ServiceType
    
    service = MicroService(
        name="test",
        host="localhost",
        port=8000,
        endpoint="/test",
        use_remote_service=True,
        service_type=ServiceType.EMBEDDING
    )
    
    assert service.name == "test"
    assert service.host == "localhost"
    assert service.port == 8000
    assert service.endpoint == "/test"
    assert service.use_remote_service is True
    assert service.service_type == ServiceType.EMBEDDING

def test_service_orchestrator():
    from comps.service import MicroService, ServiceOrchestrator, ServiceType
    
    orchestrator = ServiceOrchestrator()
    service1 = MicroService(
        name="service1",
        host="localhost",
        port=8001,
        endpoint="/test1",
        use_remote_service=True,
        service_type=ServiceType.EMBEDDING
    )
    service2 = MicroService(
        name="service2",
        host="localhost",
        port=8002,
        endpoint="/test2",
        use_remote_service=True,
        service_type=ServiceType.LLM
    )
    
    orchestrator.add(service1)
    orchestrator.add(service2)
    orchestrator.flow_to(service1, service2)
    
    assert len(orchestrator.services) == 2
    assert orchestrator.services[0] == service1
    assert orchestrator.services[1] == service2

if __name__ == "__main__":
    pytest.main([__file__]) 