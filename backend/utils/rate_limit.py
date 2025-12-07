import time
from collections import defaultdict
from fastapi import Request, HTTPException
from utils.logging import get_logger

logger = get_logger(__name__)

# In-memory storage for rate limiting (in production, use Redis or similar)
request_counts = defaultdict(list)

# Rate limit configuration: 100 requests per minute per IP
RATE_LIMIT = 100
TIME_WINDOW = 60  # seconds


async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware to prevent abuse
    """
    client_ip = request.client.host
    
    # Get current time
    current_time = time.time()
    
    # Clean old requests outside the time window
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip] 
        if current_time - req_time < TIME_WINDOW
    ]
    
    # Check if the client has exceeded the rate limit
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: 100 requests per minute"
        )
    
    # Add current request to the list
    request_counts[client_ip].append(current_time)
    
    response = await call_next(request)
    return response