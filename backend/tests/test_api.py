import pytest
from fastapi.testclient import TestClient
from main import app
from database.connection import init_db
import os
from unittest.mock import patch

client = TestClient(app)

# Mock environment variables for testing
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["CONTENT_URL"] = "https://example.com/test-content"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the RAG Chatbot Backend API"}

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "timestamp" in data

def test_status_endpoint():
    """Test the status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "initialized" in data
    assert "content_source" in data
    assert "last_updated" in data
    assert "status" in data

@patch('api.initialization_api.scrape_content_from_url')
@patch('api.initialization_api.clean_content')
@patch('api.initialization_api.preprocess_content')
@patch('api.initialization_api.create_content_chunks')
@patch('services.embedding_service.generate_embeddings')
@patch('services.vector_service.store_embeddings_batch')
def test_initialize_endpoint(mock_store_embeddings, mock_generate_embeddings, 
                           mock_create_chunks, mock_preprocess, mock_clean, mock_scrape):
    """Test the initialization endpoint"""
    # Mock return values
    mock_scrape.return_value = "Test content from URL"
    mock_clean.return_value = "Test content from URL"
    mock_preprocess.return_value = "Test content from URL"
    mock_create_chunks.return_value = ["chunk1", "chunk2"]
    mock_generate_embeddings.return_value = [[0.1, 0.2], [0.3, 0.4]]
    
    response = client.post("/api/initialize")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] in ["initializing", "failed"]

def test_query_endpoint():
    """Test the query endpoint with a sample query"""
    # First, we'll test the validation by sending an empty query
    response = client.post("/api/query", json={"query": ""})
    assert response.status_code == 400  # Should fail validation
    
    # Test with a short query (less than 3 chars)
    response = client.post("/api/query", json={"query": "hi"})
    assert response.status_code == 400  # Should fail validation
    
    # Test with a valid query (mocked to avoid external dependencies)
    with patch('services.embedding_service.generate_embedding') as mock_gen_emb, \
         patch('services.retrieval_service.find_relevant_content') as mock_find_rel, \
         patch('services.response_service.generate_response') as mock_gen_resp:
        
        mock_gen_emb.return_value = [0.1, 0.2, 0.3]
        mock_find_rel.return_value = []
        mock_gen_resp.return_value = "Test response"
        
        response = client.post("/api/query", json={"query": "What is this about?"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "sources" in data

if __name__ == "__main__":
    pytest.main()