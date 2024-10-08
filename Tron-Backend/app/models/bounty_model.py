from typing import Dict, Any

from ..schemas import bounty_schema

def serialize(bounty_detail: Dict[str, Any]) -> bounty_schema.ResponseBountyModel:
    """
    Serialize a MongoDB document into a ResponseBountyModel instance.
    
    Args:
        bounty_detail (dict): The MongoDB document representing the bounty.
    
    Returns:
        ResponseBountyModel: A Pydantic model instance of the bounty data.
    """
    return bounty_schema.ResponseBountyModel(
        gameId = bounty_detail["gameId"],
        bountyId = str(bounty_detail["_id"]),
        name = bounty_detail["name"],
        description = bounty_detail["description"],
        createdAt = bounty_detail["createdAt"],
        updatedAt = bounty_detail["updatedAt"],
    )