from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import RedirectResponse
import re

def add_security_headers(app: FastAPI):
    """
    Add security headers to the FastAPI application
    """
    
    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        # Add security headers to all responses
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        return response

def setup_cors_middleware(app: FastAPI, allowed_origins: list = None):
    """
    Setup CORS middleware for the application
    """
    if allowed_origins is None:
        # In production, you should specify your frontend domain
        allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        # Only expose headers that are necessary
        expose_headers=["Access-Control-Allow-Origin"]
    )

def setup_trusted_host_middleware(app: FastAPI, allowed_hosts: list = None):
    """
    Setup trusted host middleware to prevent host header attacks
    """
    if allowed_hosts is None:
        allowed_hosts = [".example.com", "localhost", "127.0.0.1", "[::1]"]
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts,
    )