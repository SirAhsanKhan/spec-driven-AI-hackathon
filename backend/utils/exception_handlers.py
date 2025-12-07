from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from utils.logging import get_logger

logger = get_logger(__name__)

async def http_error_handler(request: Request, exc):
    """
    Global handler for HTTP exceptions
    """
    logger.error(f"HTTP error occurred: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def validation_error_handler(request: Request, exc):
    """
    Global handler for validation errors
    """
    logger.error(f"Validation error occurred: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

async def general_exception_handler(request: Request, exc):
    """
    Global handler for general exceptions
    """
    logger.error(f"General error occurred: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred"}
    )