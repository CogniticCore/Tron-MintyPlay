from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime

class ResponseModel(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
    timestamp: datetime = None


