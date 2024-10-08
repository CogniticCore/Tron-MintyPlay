from bson import ObjectId
from datetime import datetime

from fastapi import HTTPException, status

from ..core.database import bounty_collection
from ..schemas import bounty_schema
from ..models import bounty_model

async def get_all_bounties(gameId: str):
    """
    Fetches a list of all available bounties in a game with basic metadata.
    """
    query = {"gameId": gameId}
    cursor = bounty_collection.find(query)
    
    bounties_list = [bounty_model.serialize(bounty) async for bounty in cursor]
    
    if bounties_list:
        return bounty_schema.ResponseBountyModelCollection(
            bounties=bounties_list
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bounties found for the specified game."
        )


async def get_bounty(gameId: str, bountyId: str):
    """
    Fetches a bounty in a game with basic metadata.
    """
    query = {
        "gameId": gameId,
        "_id": ObjectId(bountyId),
    }
    bounty = await bounty_collection.find_one(query)

    print(bounty)
    
    if bounty:
        return bounty_model.serialize(bounty)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bounty not found."
        )

    
async def create_bounty(gameId: str, request: bounty_schema.BountyModel):
    """
    Create a new bounty entry.
    """
    current_time = datetime.now()
    create_bounty_data = bounty_schema.CreateBountyModel(
        gameId=gameId,
        name=request.name,
        description=request.description,
        createdAt=current_time,
        updatedAt=current_time,
    )
    bounty_dict = create_bounty_data.model_dump()

    try:
        result = await bounty_collection.insert_one(bounty_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the bounty: {str(e)}"
        )

    bounty_id = str(result.inserted_id)

    return bounty_schema.ResponseCreateBountyModel(
        bountyId=bounty_id,
        createdAt=create_bounty_data.createdAt,
        updatedAt=create_bounty_data.updatedAt
    )

async def update_bounty(gameId: str, bountyId: str, request: bounty_schema.BountyModel):
    """
    Service function to update an existing bounty's data in the database.

    Args:
        gameId (str): The unique ID of the game the bounty belongs to.
        bountyId (str): The unique ID of the bounty to update.
        request (BountyModel): The new bounty data to update.

    Returns:
        dict: The newly updated bounty data.
    """
    bounty_dict = request.model_dump()
    bounty_dict["updatedAt"] = datetime.now()
    update_result = await bounty_collection.update_one(
        {"gameId": gameId, "_id": ObjectId(bountyId)},
        {"$set": bounty_dict}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bounty with ID {bountyId} not found in game {gameId}."
        )

    updated_bounty = await get_bounty(gameId, bountyId)
    return updated_bounty


async def delete_bounty(gameId: str, bountyId: str):
    """
    Service function to delete an existing bounty's data in the database.

    Args:
        gameId (str): The unique ID of the game the bounty belongs to.
        bountyId (str): The unique ID of the bounty to delete.

    Returns:
        dict: A success message if the bounty was deleted.
    """
    query = {"gameId": gameId, "_id": ObjectId(bountyId)}

    delete_result = await bounty_collection.delete_one(query)

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bounty with ID {bountyId} not found in game {gameId}."
        )

    return {"message": "Bounty successfully deleted."}

