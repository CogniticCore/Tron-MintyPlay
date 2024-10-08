from pydantic import BaseModel
from typing import List, Optional
from .orderitem_schema import ResponseCreateOrderItemCollection
from datetime import datetime

class DatabaseVerifiedPurchase(BaseModel):
    order_data: Optional[ResponseCreateOrderItemCollection]
    purchase_time: Optional[datetime]
    verification_status: Optional[str] = "Verified"
    verification_method: Optional[str] = "Automated"
    verified_by: Optional[str]
    verified_time: Optional[datetime]

class RespondVerifiedPurchase(DatabaseVerifiedPurchase):
    verifiedpurchase_id: str