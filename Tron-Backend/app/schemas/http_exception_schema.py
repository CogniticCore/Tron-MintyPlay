from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HTTPExceptionResponse(BaseModel):
    detail: str  
    error_code: Optional[int]  
    message: Optional[str] = None
    timestamp: datetime = None

