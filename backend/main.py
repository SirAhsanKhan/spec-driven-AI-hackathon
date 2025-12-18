from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from utils.exception_handlers import (
    http_error_handler,
    validation_error_handler,
    general_exception_handler
)
from utils.rate_limit import rate_limit_middleware
from utils.security import add_security_headers, setup_cors_middleware, setup_trusted_host_middleware
from utils.debugging import setup_logging, log_system_info, debug_endpoint_info
import os

# Setup logging early
setup_logging()

app = FastAPI(
    title="RAG Chatbot Backend API",
    description="API for a Retrieval-Augmented Generation (RAG) chatbot that enables users to ask questions about content from a pre-stored URL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Log system information
log_system_info()

# Setup security measures
add_security_headers(app)
setup_cors_middleware(app)
setup_trusted_host_middleware(app)

# Add middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Log endpoint information
debug_endpoint_info(app)

# Import and register routers after app initialization to prevent early failures
try:
    from api.initialization_api import router as initialization_router
    from api.status_api import router as status_router
    from api.query_api import router as query_router
    from api.health_api import router as health_router
    
    app.include_router(initialization_router, prefix="/api", tags=["initialization"])
    app.include_router(status_router, prefix="/api", tags=["status"])
    app.include_router(query_router, prefix="/api", tags=["query"])
    app.include_router(health_router, prefix="", tags=["health"])
    
    print("API routes registered successfully")
except Exception as e:
    print(f"Error importing/initializing routes: {e}")
    # Re-raise to prevent the app from starting in an incomplete state
    raise

# Manual database initialization at startup (moved from startup event)
try:
    from database.connection import init_db
    from config import validate_config
    
    # Validate configuration
    validate_config()
    print("Configuration validated successfully")
    
    # Initialize database (this might fail in serverless, but that's okay)
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Non-critical error during initialization: {e}")
    # Continue startup even if initialization fails

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Chatbot Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))