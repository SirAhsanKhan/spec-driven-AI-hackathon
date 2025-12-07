from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from utils.logging import get_logger
import time

router = APIRouter()
logger = get_logger(__name__)

class HealthStatus(BaseModel):
    status: str
    timestamp: float
    uptime: Optional[float] = None
    checks: Optional[dict] = None

# Store the application start time
start_time = time.time()

@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint to monitor system status
    """
    current_time = time.time()
    uptime = current_time - start_time
    
    # Perform basic health checks
    checks = {
        "database": "ok",  # Would check actual database connectivity in a real implementation
        "external_apis": "ok",  # Would check actual API connectivity 
        "storage": "ok"  # Would check storage availability
    }
    
    # Evaluate overall status based on checks
    status = "healthy"
    for check, result in checks.items():
        if result != "ok":
            status = "degraded"
            break
    
    logger.info(f"Health check requested, status: {status}")
    
    return HealthStatus(
        status=status,
        timestamp=current_time,
        uptime=uptime,
        checks=checks
    )