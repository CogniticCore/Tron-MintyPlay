from datetime import datetime
from typing import Dict
from ..schemas import user_schema

def serialize(user_detail: Dict) -> user_schema.UserResponse:
    games = []
    if "games" in user_detail and isinstance(user_detail["games"], list):
        games = [str(game_id) for game_id in user_detail["games"] if isinstance(game_id, str)]
    
    nfts = []
    if "nfts" in user_detail and isinstance(user_detail["nfts"], list):
        nfts = [
            user_schema.NFT(
                id=nft.get("id"),
                name=nft.get("name"),
                description=nft.get("description"),
                image=nft.get("image"),
                game=nft.get("game")
            ) for nft in user_detail["nfts"]
        ]
    
    achievements = []
    if "achievements" in user_detail and isinstance(user_detail["achievements"], list):
        achievements = [
            user_schema.Achievement(
                id=achievement.get("id"),
                name=achievement.get("name"),
                description=achievement.get("description"),
                date_achieved=str(achievement.get("date_achieved"))
            ) for achievement in user_detail["achievements"]
        ]
    
    return user_schema.UserResponse(
        user_id=str(user_detail["_id"]),
        username=user_detail["username"],
        email=user_detail["email"],
        bio=user_detail.get("bio", None),
        nfts=nfts,
        achievements=achievements,
        is_active=user_detail["is_active"],
        date_joined=str(user_detail["date_joined"]),
        games=games
    )
