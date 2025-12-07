# API Documentation for RAG Chatbot Backend

## Endpoints

### GET /
- Description: Root endpoint
- Response: `{"message": "Welcome to the RAG Chatbot Backend API"}`

### GET /docs
- Description: Interactive API documentation (Swagger UI)

### GET /redoc
- Description: Alternative API documentation (ReDoc)

### GET /health
- Description: Health check endpoint
- Response: 
  ```
  {
    "status": "healthy|degraded",
    "timestamp": 1234567890.123,
    "uptime": 1234.56,
    "checks": {
      "database": "ok",
      "external_apis": "ok",
      "storage": "ok"
    }
  }
  ```

### GET /api/status
- Description: System status and initialization information
- Response:
  ```
  {
    "initialized": true|false,
    "content_source": "URL from env var",
    "last_updated": "ISO timestamp",
    "status": "ready|not_configured"
  }
  ```

### POST /api/initialize
- Description: Initialize content from the pre-stored URL in environment variables
- Request: `{}`
- Response:
  ```
  {
    "status": "initializing|failed",
    "job_id": "unique_job_identifier"
  }
  ```

### GET /api/initialize/{job_id}
- Description: Check the status of an initialization job
- Path Parameter: job_id
- Response:
  ```
  {
    "status": "processing|completed|failed",
    "progress": 0-100,
    "url": "content source URL",
    "error": "error message if failed (optional)"
  }
  ```

### POST /api/query
- Description: Submit user query and get response
- Request: `{"query": "user's question"}`
- Response:
  ```
  {
    "response": "answer from AI",
    "sources": ["source1", "source2", ...]
  }
  ```

### POST /api/query-stream
- Description: Submit user query and get streamed response
- Request: `{"query": "user's question"}`
- Response: Stream of JSON objects with types "response_chunk", "sources", or "done"

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key (required)
- `QDRANT_HOST`: Qdrant server host (default: localhost)
- `QDRANT_API_KEY`: Qdrant API key (optional for local)
- `QDRANT_PORT`: Qdrant server port (default: 6333)
- `CONTENT_URL`: Pre-stored URL for content scraping (required)
- `DATABASE_URL`: Database connection string (default: sqlite:///./rag_chatbot.db)

## Configuration

The system is configured via environment variables. Ensure all required variables are set before running the application.