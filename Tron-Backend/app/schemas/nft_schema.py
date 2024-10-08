from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class NFTModel(BaseModel):
    gameId: str
    bountyId: str
    name: str
    description: Optional[str] = None
    uri: Optional[str] = None

class CreateNFTModel(NFTModel):
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class ResponseNFTModel(NFTModel):
    nftId: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class ResponseCreateNFTModel(BaseModel):
    nftId: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class ResponseNFTModelCollection(BaseModel):
    nfts: List[ResponseNFTModel]