from bson import ObjectId
from datetime import datetime

from fastapi import HTTPException, status

from ..core.tron import contract
from ..core.database import nft_collection
from ..schemas import nft_schema
from ..models import nft_model

async def get_all_nfts(gameId: str, bountyId: str):
    """Fetch all NFTs reward from specified bounty and game in Database"""
    query = {
        "gameId": gameId,
        "bountyId": bountyId,
    }
    cursor = nft_collection.find(query)
    
    nfts_list = [nft_model.serialize(nft) async for nft in cursor]
    
    if nfts_list:
        return nft_schema.ResponseNFTModelCollection(
            nfts=nfts_list
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No nfts found for the specified bountyId & gameId."
        )
    
async def get_nft(gameId: str, bountyId: str, nftId: str):
    """Fetch a NFT reward from specified nft, bounty, game in Database"""
    query = {
        "gameId": gameId,
        "bountyId": bountyId,
        "_id": ObjectId(nftId),
    }
    nft = await nft_collection.find_one(query)
    
    if nft:
        return nft_model.serialize(nft)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bounty not found."
        )

async def create_nft(gameId: str, bountyId: str, request: nft_schema.NFTModel):
    """
    Create a new NFT entry.
    """
    current_time = datetime.now()
    
    create_nft_data = nft_schema.CreateNFTModel(
        gameId=gameId,
        bountyId=bountyId,
        name=request.name,
        description=request.description,
        uri=request.uri,
        createdAt=current_time,
        updatedAt=current_time,
    )
    nft_dict = create_nft_data.model_dump()

    try:
        result = await nft_collection.insert_one(nft_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the NFT: {str(e)}"
        )

    nft_id = str(result.inserted_id)

    return nft_schema.ResponseCreateNFTModel(
        nftId = nft_id,
        createdAt=  create_nft_data.createdAt,
        updatedAt = create_nft_data.updatedAt,
    )

async def update_nft(gameId: str, bountyId: str, nftId: str, request: nft_schema.NFTModel):
    """
    Service function to update an existing NFT's data in the database.

    Args:
        gameId (str): The unique ID of the game the NFT belongs to.
        bountyId (str): The unique ID of the bounty associated with the NFT.
        nftId (str): The unique ID of the NFT to update.
        request (NFTModel): The new NFT data to update.

    Returns:
        dict: The newly updated NFT data.
    """
    nft_dict = request.model_dump()
    nft_dict["updatedAt"] = datetime.now()

    update_result = await nft_collection.update_one(
        {"gameId": gameId, "bountyId": bountyId, "_id": ObjectId(nftId)},
        {"$set": nft_dict}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NFT with ID {nftId} not found in game {gameId} and bounty {bountyId}."
        )

    updated_nft = await get_nft(gameId, bountyId, nftId)  
    return updated_nft

async def delete_nft(gameId: str, bountyId: str, nftId: str):
    """
    Service function to delete an existing NFT's data in the database.

    Args:
        gameId (str): The unique ID of the game the NFT belongs to.
        bountyId (str): The unique ID of the bounty associated with the NFT.
        nftId (str): The unique ID of the NFT to delete.

    Returns:
        dict: A success message if the NFT was deleted.
    """
    query = {"gameId": gameId, "bountyId": bountyId, "_id": ObjectId(nftId)}

    delete_result = await nft_collection.delete_one(query)

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NFT with ID {nftId} not found in game {gameId} and bounty {bountyId}."
        )

    return {"message": "NFT successfully deleted."}



async def get_nft_owner(tokenId: int):
    """Service Function to retrieve NFT Owner's Address from TokenId"""
    try:
        address = contract.functions.ownerOf(1)
        return address
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NFT with tokenId {tokenId} does not exist"
        )

# async def mint_nft(user_wallet: str, game_id: str):
#     # Get game metadata and user info from MongoDB
#     game_metadata = await get_game_metadata(game_id)
    
#     # Interact with the smart contract to mint the NFT
#     tx = client.trx.create_smart_contract_function(
#         contract_address,
#         'mintNFT',
#         [user_wallet, game_metadata['nftURI']]
#     ).sign().broadcast()

#     # Log the transaction in MongoDB
#     await save_nft_to_mongo(user_wallet, tx['transaction_id'], game_metadata['nftURI'])

#     return {"status": "success", "transaction_id": tx['transaction_id']}
