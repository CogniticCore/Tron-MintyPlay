from fastapi import APIRouter, status
from ....schemas import orderitem_schema
from ....services import orderitem_service
from ....schemas.orderitem_schema import CreateOrderItem, CreateOrderItemCollection
from ....schemas.response_schema import ResponseModel
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = '/orderitem',
    tags=['orderitem']
)

@router.post('/items/price', status_code=status.HTTP_200_OK)
async def get_price(request: CreateOrderItem): 
    price = await orderitem_service.get_price(request)

    return ResponseModel(
        status="success",
        message="Game price retrieved successfully",
        data=price,
        timestamp=datetime.now().isoformat()
    )

@router.post('/create', status_code=status.HTTP_200_OK)
async def create_buy_order(request: CreateOrderItemCollection): 
    price = await orderitem_service.create_buy_order(request)

    return ResponseModel(
        status="success",
        message="Game price retrieved successfully",
        data=price,
        timestamp=datetime.now().isoformat()
    )

