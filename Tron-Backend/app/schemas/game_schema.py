from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Reward(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Review(BaseModel):
    user_id: Optional[str] = None
    user: Optional[str] = None
    avatar: Optional[str] = None
    rating: Optional[float] = None
    comment: Optional[str] = None

class SystemRequirements(BaseModel):
    os: Optional[str] = None
    processor: Optional[str] = None
    memory: Optional[str] = None
    graphics: Optional[str] = None
    storage: Optional[str] = None

class DeveloperData(BaseModel):
    name: Optional[str] = None
    wallet_address: Optional[str] = None

class GameModel(BaseModel):
    id: Optional[str]
    title: Optional[str] = None
    price: Optional[float] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    nftRewards: Optional[List[Reward]] = None
    images: Optional[List[str]] = None #url
    tags: Optional[List[str]] = None
    rating: Optional[float] = None
    systemRequirements: Optional[SystemRequirements] = None
    developerData: Optional[DeveloperData] = None

class CreateGameModel(GameModel):
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    reviews: Optional[List[Review]] = None

class ResponseGameModel(GameModel):
    game_id: Optional[str]
    id: Optional[str]
    createdAt: Optional[datetime] 
    updatedAt: Optional[datetime]
    reviews: Optional[List[Review]] = None

class ResponseCreateGameModel(BaseModel):
    game_id: Optional[str]
    id: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    reviews: Optional[List[Review]] = None

class GameModelCollection(BaseModel):
    games: Optional[List[ResponseGameModel]]


