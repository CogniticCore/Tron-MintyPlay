from typing import Dict, Any

from ..schemas import nft_schema

def serialize(nft_detail: Dict[str, Any]) -> nft_schema.ResponseNFTModel:
    """
    Serialize a MongoDB document into a ResponseNFTModel instance.

    Args:
        nft_detail (dict): The MongoDB document representing the NFT.

    Returns:
        ResponseNFTModel: A Pydantic model instance of the NFT data.
    """
    return nft_schema.ResponseNFTModel(
        gameId=nft_detail["gameId"],
        bountyId=nft_detail["bountyId"],
        nftId=str(nft_detail["_id"]),
        name=nft_detail["name"],
        description=nft_detail["description"],
        uri=nft_detail["uri"],
        createdAt=nft_detail["createdAt"],
        updatedAt=nft_detail["updatedAt"],
    )