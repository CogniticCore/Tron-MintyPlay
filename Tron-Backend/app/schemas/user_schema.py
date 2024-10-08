from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from .orderitem_schema import ResponseCreateOrderItemCollection
from .game_schema import GameModelCollection

class UserBase(BaseModel):
    """
    Base model for user details.
    """
    username: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    pass

class NFT(BaseModel):
    id: int
    name: str
    description: str
    image: str
    game: str

class Achievement(BaseModel):
    id: int
    name: str
    description: str
    date_achieved: datetime

class DatabaseUserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    bio: Optional[str] = None
    nfts: Optional[List[NFT]] = []
    achievements: Optional[List[Achievement]] = []
    is_active: bool
    date_joined: datetime
    games: Optional[List[str]]

class UserResponse(BaseModel):
    """
    Response model for returning user details.
    """
    user_id: str
    username: str
    email: EmailStr
    bio: Optional[str] = None
    nfts: Optional[List[NFT]] = []
    achievements: Optional[List[Achievement]] = []
    is_active: bool
    date_joined: datetime
    games: Optional[List[str]]
    
