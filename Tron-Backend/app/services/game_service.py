import logging
from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException, status

from ..schemas import game_schema
from ..core.database import game_collection
from ..models.game_model import serialize

logger = logging.getLogger(__name__)

async def get_all_games():
    """
    Service function to retrieve all game data from the database.
    
    Args:
        None

    Returns:
        list[dict]: Game data if found.
    """
    query = {}
    cursor = game_collection.find(query)  
    if cursor:
        games_list = [serialize(game) async for game in cursor]
        return game_schema.GameModelCollection(
            games = games_list
        ) 
    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="An error occurred while retrieving all game data."
        )
    
async def get_game(gameId: str):
    """
    Service function to retrieve a single game's data by gameId.

    Args:
        gameId (str): The unique ID of the game.

    Returns:
        dict: Game data if found.
    """
    query = {"_id": ObjectId(gameId)}
    result = await game_collection.find_one(query)

    if result is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Game with ID {gameId} not found."
            )
    else: 
        return serialize(result)

async def create_game(request: game_schema.GameModel):
    """
    Service function to create a new game in the database.

    Args:
        request (GameCreate): The game creation data from the request.

    Returns:
        dict: The newly created game data.
    """
    existing_game = await game_collection.find_one({'title': request.title})
    existing_id = await game_collection.find_one({'title': request.id})
    if existing_game or existing_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A game with the title '{request.title}' or A game with the id '{request.existing_id} already exists."
        )
    
    current_time = datetime.now()
    create_game_data = game_schema.CreateGameModel(
        id = request.id,
        title = request.title,
        price = request.price,
        genre = request.genre,
        description = request.description,
        nftRewards = request.nftRewards,
        tags = request.tags,
        rating = request.rating,
        reviews = [],
        systemRequirements = request.systemRequirements,
        developerData = request.developerData,
        createdAt = current_time,
        updatedAt = current_time,
    )
    game_dict = create_game_data.model_dump()

    result = await game_collection.insert_one(game_dict)

    if result:
    
        game_id = str(result.inserted_id)
        
        return game_schema.ResponseCreateGameModel(
            game_id=game_id,
            id=create_game_data.id,
            createdAt=create_game_data.createdAt,
            updatedAt=create_game_data.updatedAt
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An error occurred while creating the game."
        )

async def update_game(gameId: str, request: game_schema.GameModel):
    """
    Service function to update an existing game's data in the database.

    Args:
        gameId (str): The unique ID of the game to update.
        request (GameModel): The new game data to update.

    Returns:
        dict: The newly updated game data.
    """
    game_dict = request.model_dump()
    game_dict["updatedAt"] = datetime.now()

    update_result = await game_collection.update_one(
        {"_id": ObjectId(gameId)},
        {"$set": game_dict}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {gameId} not found."
        )

    updated_game = await get_game(gameId) 
    return updated_game

async def delete_game(gameId: str):
    """
    Service function to delete an existing game's data in the database.

    Args:
        gameId (str): The unique ID of the game to delete.

    Returns:
        dict: A success message if the game was deleted.
    """
    query = {"_id": ObjectId(gameId)}

    # Attempt to delete the game
    delete_result = await game_collection.delete_one(query)

    # Check if the game was deleted (deleted_count > 0 means it was deleted)
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {gameId} not found."
        )

    # Return a success message
    return {"message": "Game successfully deleted."}