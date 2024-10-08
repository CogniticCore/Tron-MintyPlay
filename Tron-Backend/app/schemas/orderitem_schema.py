from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BaseOrderItem(BaseModel):
    game_id: str
    quantity: int

class CreateOrderItem(BaseOrderItem):
    pass

class RespondOrderItemCreate(BaseOrderItem):
    price: float

class CreateOrderItemCollection(BaseModel):
    user_id: Optional[str] = None
    OrderItemCollection: Optional[List[CreateOrderItem]] = None

class DatabaseCreateOrderItemCollection(BaseModel):
    user_id: Optional[str] = None
    OrderItemCollection: Optional[List[CreateOrderItem]] = None
    total_quantity: Optional[int] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    transaction: Optional[str] = None
    created_time: Optional[datetime] = None

class ResponseCreateOrderItemCollection(BaseModel):
    order_id: Optional[str] = None
    user_id: Optional[str] = None
    OrderItemCollection: Optional[List[CreateOrderItem]] = None
    total_quantity: Optional[int] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    transaction: Optional[str] = None
    created_time: Optional[datetime] = None