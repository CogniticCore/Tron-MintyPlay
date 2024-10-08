from datetime import datetime
from typing import Set

from bson import ObjectId
from fastapi import HTTPException, status

from ..core.database import (
    orderitem_collection,
    user_collection,
    verifiedpurchase_collection,
)
from ..schemas.orderitem_schema import ResponseCreateOrderItemCollection
from ..schemas.purchase_schema import CreatePurchase
from ..schemas.verifiedpurchase_schema import (
    DatabaseVerifiedPurchase,
    RespondVerifiedPurchase,
)

import logging

logger = logging.getLogger(__name__)


async def purchase(request: CreatePurchase) -> RespondVerifiedPurchase:
    """
    Process a purchase request.

    Steps:
    1. Validate user existence.
    2. Validate order and transaction status.
    3. Verify the transaction.
    4. Update order status.
    5. Store verified purchase.
    6. Update user's purchased games.
    7. Return response.
    """
    user_id = request.user_id
    transaction_id = request.wallet_id
    order_id = request.order_id

    # Step 1: Validate user existence
    user_data = await get_user_by_id(user_id)

    # Step 2: Validate order and transaction status
    order_data = await get_order_by_id(order_id)
    validate_order_status(order_data)
    await validate_transaction_uniqueness(transaction_id)

    # Step 3: Verify the transaction
    if not verify_transaction(transaction_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction ID {transaction_id} cannot be verified.",
        )

    # Step 4: Update order status
    await update_order_status(order_id, transaction_id)

    #step 4.5 call Updated order
    order_data = await get_order_by_id(order_id)

    # Step 5: Store verified purchase
    verified_purchase_id = await store_verified_purchase(order_data, transaction_id)

    # Step 6: Update user's purchased games
    await update_user_games(user_data, order_data)

    # Step 7: Return response
    response = await create_response(
        verified_purchase_id, order_data, transaction_id
    )
    return response


async def get_user_by_id(user_id: str) -> dict:
    """Retrieve user data by user ID."""
    try:
        user_object_id = ObjectId(user_id)
    except Exception as e:
        logger.error(f"Invalid user ID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID: {user_id}",
        ) from e

    user_data = await user_collection.find_one({"_id": user_object_id})
    if not user_data:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )
    return user_data


async def get_order_by_id(order_id: str) -> dict:
    """Retrieve order data by order ID."""
    try:
        order_object_id = ObjectId(order_id)
    except Exception as e:
        logger.error(f"Invalid order ID format: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order ID: {order_id}",
        ) from e

    order_data = await orderitem_collection.find_one({"_id": order_object_id})
    if not order_data:
        logger.error(f"Order not found: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found.",
        )
    return order_data


def validate_order_status(order_data: dict):
    """Check if the order has already been completed."""
    if order_data.get("status") == "Completed":
        logger.warning(f"Order already completed: {order_data['_id']}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order with ID {order_data['_id']} has already been completed.",
        )


async def validate_transaction_uniqueness(transaction_id: str):
    """Ensure the transaction ID hasn't been used before."""
    existing_transaction = await verifiedpurchase_collection.find_one(
        {"transaction_id": transaction_id}
    )
    if existing_transaction:
        logger.warning(f"Transaction ID already verified: {transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction ID {transaction_id} has already been verified.",
        )


def verify_transaction(transaction_id: str) -> bool:
    """
    Verify the transaction.

    Replace this with actual verification logic.
    """
    # TODO: Implement actual transaction verification logic.
    logger.info(f"Verifying transaction ID: {transaction_id}")
    return True  # Mocked as always true for now.


async def update_order_status(order_id: str, transaction_id: str):
    """Update the order status to 'Completed' and set the transaction ID."""
    result = await orderitem_collection.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "status": "Completed",
                "transaction": transaction_id,
            }
        },
    )
    if result.matched_count == 0:
        logger.error(f"Failed to update order status: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found.",
        )
    logger.info(f"Order status updated to 'Completed' for order ID: {order_id}")


async def store_verified_purchase(order_data: dict, transaction_id: str) -> str:
    """Store the verified purchase in the database."""
    current_time = datetime.now()

    response_order_data = ResponseCreateOrderItemCollection(
        order_id=str(order_data["_id"]),
        user_id=order_data["user_id"],
        OrderItemCollection=order_data["OrderItemCollection"],
        total_quantity=order_data["total_quantity"],
        total_price=order_data["total_price"],
        status=order_data["status"],
        transaction=order_data["transaction"],
        created_time=order_data["created_time"],
    )

    verified_purchase = DatabaseVerifiedPurchase(
        order_data=response_order_data,
        purchase_time=current_time,
        verification_status="Verified",
        verification_method="Automated",
        verified_by="Automated-Verifier",
        verified_time=current_time,
        transaction_id=transaction_id,
    )

    result = await verifiedpurchase_collection.insert_one(
        verified_purchase.model_dump()
    )
    if not result.acknowledged:
        logger.error("Failed to store verified purchase.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while storing the verified purchase.",
        )
    logger.info(f"Verified purchase stored with ID: {result.inserted_id}")
    return str(result.inserted_id)


async def update_user_games(user_data: dict, order_data: dict):
    """Update the user's purchased games."""
    user_id = user_data["_id"]
    current_games: Set[str] = set(user_data.get("games", []))
    new_games: Set[str] = {
        item["game_id"] for item in order_data["OrderItemCollection"]
    }

    # Merge and update games
    updated_games = list(current_games.union(new_games))
    result = await user_collection.update_one(
        {"_id": user_id},
        {"$set": {"games": updated_games}},
    )
    if result.matched_count == 0:
        logger.error(f"Failed to update games for user ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update games for user ID: {user_id}",
        )
    logger.info(f"User games updated for user ID: {user_id}")


async def create_response(
    verified_purchase_id: str, order_data: dict, transaction_id: str
) -> RespondVerifiedPurchase:
    """Create the response object to return to the client."""
    current_time = datetime.now()

    response_order_data = ResponseCreateOrderItemCollection(
        order_id=str(order_data["_id"]),
        user_id=order_data["user_id"],
        OrderItemCollection=order_data["OrderItemCollection"],
        total_quantity=order_data["total_quantity"],
        total_price=order_data["total_price"],
        status=order_data["status"],
        transaction=transaction_id,
        created_time=order_data["created_time"],
    )

    response = RespondVerifiedPurchase(
        verifiedpurchase_id=verified_purchase_id,
        order_data=response_order_data,
        purchase_time=current_time,
        verification_status="Verified",
        verification_method="Automated",
        verified_by="System",
        verified_time=current_time,
    )
    logger.info(f"Responding with verified purchase ID: {verified_purchase_id}")
    return response
