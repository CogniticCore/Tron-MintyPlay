from pydantic import BaseModel
from typing import List

class BasePurchase(BaseModel):
    user_id: str
    order_id: str
    transaction_id: str

class CreatePurchase(BasePurchase):
    pass
