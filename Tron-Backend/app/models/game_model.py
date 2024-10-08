from typing import Dict, Any

from ..schemas import game_schema

def serialize(game_detail: Dict[str, Any]) -> game_schema.ResponseGameModel:
    """
    Serialize a MongoDB document into a ResponseGameModel instance.
    
    Args:
        game (dict): The MongoDB document representing the game.
    
    Returns:
        ResponseGameModel: A Pydantic model instance of the game data.
    """
    return game_schema.ResponseGameModel(
        game_id=str(game_detail["_id"]),
        id=game_detail["id"],
        title=game_detail.get("title"),
        price=game_detail.get("price"),
        genre=game_detail.get("genre"),
        description=game_detail.get("description"),
        nftRewards=game_detail.get("nftRewards", []),  # Default to an empty list if key is missing
        images=game_detail.get("images", []),  # Default to an empty list if key is missing
        tags=game_detail.get("tags", []),  # Default to an empty list if key is missing
        rating=game_detail.get("rating"),
        systemRequirements=game_detail.get("systemRequirements"),
        developerData=game_detail.get("developerData"),
        createdAt=game_detail.get("createdAt"),
        updatedAt=game_detail.get("updatedAt"),
        reviews=game_detail.get("reviews", [])  # Default to an empty list if key is missing
    )