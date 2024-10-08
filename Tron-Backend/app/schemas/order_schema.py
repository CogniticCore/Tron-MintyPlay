from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .orderitem_schema import OrderItemCreate, OrderItemResponse
# Order Schema
class OrderBase(BaseModel):
    total: float
    status: str
    payment_status: str
    created_at: datetime

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    user_id: int
    items: List[OrderItemResponse]
    transaction_id: str