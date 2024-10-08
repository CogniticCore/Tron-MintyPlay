from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class BountyModel(BaseModel):
    gameId: str
    name: str
    description: str

class CreateBountyModel(BountyModel):
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class ResponseBountyModel(BountyModel):
    bountyId: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class ResponseCreateBountyModel(BaseModel):
    bountyId: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class ResponseBountyModelCollection(BaseModel):
    bounties: List[ResponseBountyModel]