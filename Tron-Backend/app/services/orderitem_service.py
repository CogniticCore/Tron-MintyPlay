from ..schemas import orderitem_schema
from ..schemas.orderitem_schema import CreateOrderItem, RespondOrderItemCreate, CreateOrderItemCollection, ResponseCreateOrderItemCollection, DatabaseCreateOrderItemCollection
from ..core.database import orderitem_collection, game_collection, user_collection
from ..models.game_model import serialize

import logging
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from fastapi import status
from typing import Set, List

logger = logging.getLogger(__name__)

async def get_price(request: CreateOrderItem) -> RespondOrderItemCreate:
    try:
        game_id = request.game_id
        quantity = request.quantity

        query = {"_id" : ObjectId(game_id)}
        target_game = await game_collection.find_one(query)

        if quantity is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quantity is missing."
            )
        
        if quantity != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"quantity can only be 1"
            )

        if target_game is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail= f"Game with ID {game_id} not found."
                )
        
        price = target_game.get("price")
        if price is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Price is missing for game with ID {game_id}."
            )

        return RespondOrderItemCreate(
            game_id=game_id,
            quantity=quantity,
            price=price
        )
    
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"There was an internal error while fetching gamedata :{e}"
            )

async def create_buy_order(request: CreateOrderItemCollection) -> ResponseCreateOrderItemCollection:

    '''
    1. Check if the user already owns any of the games in the order.
    2. Ensure there are no duplicate games within the current order.
    3. Prevent multiple orders for the same games while the status is still pending or processing.
    '''
    # Fetch user data to check currently owned games
    user_data = await user_collection.find_one({'_id': ObjectId(request.user_id)})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {request.user_id} not found."
        )
    
    # Fetch current games owned by the user
    current_games: Set[str] = {game for game in user_data.get("games", [])}
    
    # Extract game_ids from the order request
    new_games: List[str] = [item.game_id for item in request.OrderItemCollection]
    
    # 1. Check if any games in the order are already owned by the user
    duplicates_in_owned_games = current_games.intersection(new_games)
    if duplicates_in_owned_games:
        duplicate_games = ', '.join(duplicates_in_owned_games)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already own the following games: {duplicate_games}. Please remove them from your order."
        )
    
    # 2. Check for duplicates within the order itself
    if len(new_games) != len(set(new_games)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The order contains duplicate games. Please review your order."
        )
    
    # 3. Prevent multiple orders for the same games while status is still pending or processing
    existing_order = await orderitem_collection.find_one({
        'user_id': request.user_id,
        'status': {"$in": ["Pending", "Processing"]},
        'OrderItemCollection.game_id': {"$in": new_games}
    })
    
    if existing_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an ongoing order for one or more of these games."
        )
    
    # Calculate total price and total quantity of the order
    total_price = 0
    total_quantity = 0

    for item in request.OrderItemCollection:
        item_attribute = await get_price(item)  # This assumes you have a function that gets the price and other attributes
        total_quantity += item_attribute.quantity
        total_price += item_attribute.price

    # Prepare the purchase item collection
    purchaseitems = DatabaseCreateOrderItemCollection(
        user_id=request.user_id,
        OrderItemCollection=request.OrderItemCollection,
        total_quantity=total_quantity,
        total_price=total_price,
        status="Pending",
        transaction=None,
        created_time=datetime.now()
    )

    # Insert the purchase into the order collection
    purchase_items_dict = purchaseitems.model_dump()

    result = await orderitem_collection.insert_one(purchase_items_dict)
    order_id = str(result.inserted_id)

    # Return the response
    return ResponseCreateOrderItemCollection(
        order_id=order_id,
        user_id=request.user_id,
        OrderItemCollection=request.OrderItemCollection,
        total_quantity=total_quantity,
        total_price=total_price,
        status=purchaseitems.status,
        transaction=purchaseitems.transaction,
        created_time=purchaseitems.created_time
    )
