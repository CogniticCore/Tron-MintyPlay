import logging
from datetime import datetime

from fastapi import APIRouter, status

from ....schemas import response_schema, nft_schema
from ....services import nft_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = '/nfts',
    tags=['nfts']
)

@router.get('/{gameId}/{bountyId}', status_code = status.HTTP_200_OK)
async def get_all_nfts(gameId: str, bountyId: str):
    """Fetch all NFTs reward from specified bounty and game in Database"""
    list_nfts = await nft_service.get_all_nfts(gameId, bountyId)
    return response_schema.ResponseModel(
        status="success",
        message="Retrieve All NFTs successfully",
        data=list_nfts,
        timestamp=datetime.now().isoformat()
    )

@router.get('/{gameId}/{bountyId}/{nftId}', status_code = status.HTTP_200_OK)
async def get_nft(gameId: str, bountyId: str, nftId: str):
    """Fetch a NFT reward from specified nft, bounty, game in Database"""
    nft = await nft_service.get_nft(gameId, bountyId, nftId)
    return response_schema.ResponseModel(
        status="success",
        message="Retrieve NFT successfully",
        data=nft,
        timestamp=datetime.now().isoformat()
    )

@router.post('/{gameId}/{bountyId}', status_code = status.HTTP_201_CREATED)
async def create_nfts(gameId: str, bountyId: str, request: nft_schema.NFTModel):
    """Create a new NFT entry."""
    nft_detail = await nft_service.create_nft(gameId, bountyId, request)
    return response_schema.ResponseModel(
        status="success",
        message="Create New NFT successfully",
        data=nft_detail,
        timestamp=datetime.now().isoformat()
    )

@router.put('/{gameId}/{bountyId}/{nftId}/', status_code=status.HTTP_200_OK)
async def update_nft(gameId: str, bountyId: str, nftId: str, request: nft_schema.NFTModel):
    """
    Update an existing NFT entry.
    """
    updated_nft = await nft_service.update_nft(gameId, bountyId, nftId, request)
    return response_schema.ResponseModel(
        status="success",
        message=f"NFT with ID {nftId} in game {gameId} and bounty {bountyId} updated successfully",
        data=updated_nft,
        timestamp=datetime.now().isoformat()
    )

@router.delete('/{gameId}/{bountyId}/{nftId}/', status_code=status.HTTP_200_OK)
async def delete_nft(gameId: str, bountyId: str, nftId: str):
    """
    Delete an existing NFT entry.
    """
    data = await nft_service.delete_nft(gameId, bountyId, nftId)
    return response_schema.ResponseModel(
        status="success",
        message=f"NFT with ID {nftId} in game {gameId} and bounty {bountyId} deleted successfully",
        data=data,
        timestamp=datetime.now().isoformat()
    )


@router.get('/{tokenId}/owner', status_code=status.HTTP_200_OK)
async def get_nft_owner(tokenId: int):
    """Fetch an NFT Owner's Address from nft tokenId on Blockchain"""
    address = await nft_service.get_nft_owner(tokenId)
    return response_schema.ResponseModel(
        status="success",
        message="Retrieve Owner's Address successfully",
        data=address,
        timestamp=datetime.now().isoformat()
    )

# @router.get('/mint', status_code=status.HTTP_200_OK)
# async def mint_nft(user_wallet: str, game_id: str):
#     """Mints an NFT after a player wins a game (interacts with blockchain)."""

#     nft_data = await nft_service.mint_nft(user_wallet, game_id)
    
    # return response_schema.ResponseModel(
    #     status="success",
    #     message="Minting Reward successfully",
    #     data=nft_data,
    #     timestamp=datetime.now().isoformat()
    # )