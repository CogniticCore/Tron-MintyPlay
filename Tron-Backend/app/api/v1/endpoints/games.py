import logging
from datetime import datetime

from fastapi import APIRouter, status

from ....schemas import game_schema, response_schema
from ....services import game_service 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = '/games',
    tags=['games']
)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_games(): 
    """
    Fetches a list of all available games with basic metadata.
    """
    game_data = await game_service.get_all_games()
    return response_schema.ResponseModel(
        status="success",
        message="Game retrieved successfully",
        data=game_data,
        timestamp=datetime.now().isoformat()
    )

@router.get('/{gameId}', status_code=status.HTTP_200_OK)
async def get_game(gameId: str): 
    """
    Retrieves detailed information about a specific game by its ID.
    """
    game_data = await game_service.get_game(gameId)
    return response_schema.ResponseModel(
        status="success",
        message="Game retrieved successfully",
        data=game_data,
        timestamp=datetime.now().isoformat()
    )

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_game(request: game_schema.GameModel):
    """
    Create a new game entry.
    """
    game_data = await game_service.create_game(request)
    return response_schema.ResponseModel(
        status="success",
        message="Game created successfully",
        data=game_data,
        timestamp=datetime.now().isoformat()
    )

@router.put('/{gameId}', status_code=status.HTTP_202_ACCEPTED)
async def update_game(gameId: str, request: game_schema.GameModel):
    """
    Updates the details of an existing game.
    """
    updated_game = await game_service.update_game(gameId, request)
    
    return response_schema.ResponseModel(
        status="success",
        message="Successfully updated game data",
        data=updated_game,
        timestamp=datetime.now().isoformat()
    )
    

@router.delete('/{gameId}', status_code=status.HTTP_202_ACCEPTED)
async def delete_game(gameId: str):
    """
    Updates the details of an existing game.
    """
    delete_game = await game_service.delete_game(gameId)

    return response_schema.ResponseModel(
        status="success",
        message="Successfully deleted game data",
        data=delete_game,
        timestamp=datetime.now().isoformat()
    )

