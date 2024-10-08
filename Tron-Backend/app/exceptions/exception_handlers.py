from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import logging
from ..schemas.http_exception_schema import HTTPExceptionResponse  # Import the model

# Set up logging
logger = logging.getLogger("fastapi_error_handler")
logging.basicConfig(level=logging.INFO)

async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for HTTPException"""
    
    logger.error(f"HTTPException: {exc.detail}, Path: {request.url.path}")

    response_data = HTTPExceptionResponse(
        detail=exc.detail if exc.detail else "An error occurred",
        error_code=exc.status_code,
        message="An error occurred",
        timestamp=datetime.now().isoformat()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data.model_dump()
    )
