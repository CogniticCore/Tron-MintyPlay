import logging
from datetime import datetime

from fastapi import APIRouter, status

from ....schemas import response_schema, purchase_schema
from ....services import purchase_service 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = '/purchases',
    tags=['purchases']
)

@router.post('/', status_code=status.HTTP_200_OK)
async def purchase(request: purchase_schema.CreatePurchase): 
    """
    Fetches a list of all available games with basic metadata.
    """
    game_data = await purchase_service.purchase(request)
    return response_schema.ResponseModel(
        status="success",
        message="Purchase successfully",
        data=game_data,
        timestamp=datetime.now()
    )