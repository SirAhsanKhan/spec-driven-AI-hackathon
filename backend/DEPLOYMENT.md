# Deployment Instructions for RAG Chatbot Backend

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (optional, for containerized deployment)

## Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
CONTENT_URL=https://example.com/content-to-scrape

# Optional (with defaults)
QDRANT_HOST=localhost
QDRANT_API_KEY=your_qdrant_api_key_if_using_cloud
QDRANT_PORT=6333
DATABASE_URL=sqlite:///./rag_chatbot.db
```

## Running the Application

### Option 1: Direct Execution

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Option 2: Using Docker Compose

1. Build and run the services:
   ```bash
   docker-compose up --build
   ```

2. To run in detached mode:
   ```bash
   docker-compose up --build -d
   ```

## Initializing Content

1. After starting the application, initialize the content from your pre-stored URL:
   ```bash
   curl -X POST http://localhost:8000/api/initialize
   ```

2. This will return a job ID. Check the status of the initialization:
   ```bash
   curl http://localhost:8000/api/initialize/{job_id}
   ```

## API Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Deployment Considerations

1. Use a production-grade database (PostgreSQL instead of SQLite)
2. Add a reverse proxy (nginx)
3. Set up proper logging aggregation
4. Implement proper monitoring and alerting
5. Use a proper WSGI/ASGI server (like Gunicorn with Uvicorn worker)
6. Ensure proper security headers and CORS settings
7. Set up SSL certificates

## Docker Production Deployment

For production, use the following command to run with proper resource limits:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

(You would create a docker-compose.prod.yml with production-specific settings)