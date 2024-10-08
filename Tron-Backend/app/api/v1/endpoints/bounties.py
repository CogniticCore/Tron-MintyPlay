import logging
from datetime import datetime

from fastapi import APIRouter, status

from ....schemas import bounty_schema, response_schema
from ....services import bounty_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = '/bounties',
    tags=['bounties']
)

@router.get('/{gameId}', status_code=status.HTTP_200_OK)
async def get_all_bounties(gameId: str):
    """
    Fetches a list of all available bounties in a game with basic metadata.
    """
    bounties = await bounty_service.get_all_bounties(gameId)
    return response_schema.ResponseModel(
        status="success",
        message=f"All bounties from game {gameId} retrieved successfully",
        data=bounties,
        timestamp=datetime.now().isoformat()
    )

@router.get('/{gameId}/{bountyId}', status_code=status.HTTP_200_OK)
async def get_bounty(gameId: str, bountyId: str):
    """
    Fetches a list of all available bounties in a game with basic metadata.
    """
    bounties = await bounty_service.get_bounty(gameId, bountyId)
    return response_schema.ResponseModel(
        status="success",
        message=f"Bounty {bountyId} from game {gameId} retrieved successfully",
        data=bounties,
        timestamp=datetime.now().isoformat()
    )

@router.post('/{gameId}/', status_code=status.HTTP_201_CREATED)
async def create_bounty(gameId: str, request: bounty_schema.BountyModel):
    """
    Create a new bounty entry.
    """
    bounty_detail = await bounty_service.create_bounty(gameId, request)
    return response_schema.ResponseModel(
        status="success",
        message=f"Bounty inside the game {gameId} created successfully",
        data=bounty_detail,
        timestamp=datetime.now().isoformat()
    )

@router.put('/{gameId}/{bountyId}/', status_code=status.HTTP_200_OK)
async def update_bounty(gameId: str, bountyId: str, request: bounty_schema.BountyModel):
    """
    Update an existing bounty entry.
    """
    updated_bounty = await bounty_service.update_bounty(gameId, bountyId, request)
    return response_schema.ResponseModel(
        status="success",
        message=f"Bounty with ID {bountyId} in game {gameId} updated successfully",
        data=updated_bounty,
        timestamp=datetime.now().isoformat()
    )

@router.delete('/{gameId}/{bountyId}/', status_code=status.HTTP_200_OK)
async def delete_bounty(gameId: str, bountyId: str):
    """
    Delete an existing bounty entry.
    """
    data = await bounty_service.delete_bounty(gameId, bountyId)
    return response_schema.ResponseModel(
        status="success",
        message=f"Bounty with ID {bountyId} in game {gameId} deleted successfully",
        data=data,
        timestamp=datetime.now().isoformat()
    )



