from ....schemas import user_schema, response_schema
from ....services import user_service

from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter(
    prefix = '/users',
    tags=['users']
)

@router.get('/{userId}/purchases')
def get_purchased_games(userId: str):
    """
    Fetches the list of games purchased by a specific user.
    """
    purchased_games = user_service.get_purchased_games(userId)

    return response_schema.ResponseModel(
        status="success",
        message="successfully register an account",
        data=purchased_games,
        timestamp=datetime.now().isoformat()
    )

@router.get('/{userId}/nfts')
def get_purchased_nfts(userId: str):
    """
    Fetches the list of nfts purchased by a specific user.
    """

    purchased_nfts = user_service.get_purchased_nfts(userId) 

    return response_schema.ResponseModel(
        status="success",
        message="successfully register an account",
        data=purchased_nfts,
        timestamp=datetime.now().isoformat()
    )

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(request: user_schema.UserCreate):
    """
    register
    """
    user_data = await user_service.register(request)

    return response_schema.ResponseModel(
        status="success",
        message="successfully register an account",
        data=user_data,
        timestamp=datetime.now().isoformat()
    )

@router.get('/login')
def login(userId: str):
    """
    login
    """
    return user_service.login(userId)

###WILLDELETELATER###
###WILLDELETELATER###
###WILLDELETELATER###
@router.get('/all_user')
async def all_user():
    all_user = await user_service.all_user()

    return response_schema.ResponseModel(
        status="success",
        message="successfully register an account",
        data=all_user,
        timestamp=datetime.now().isoformat()
    )
###WILLDELETELATER###
###WILLDELETELATER###
###WILLDELETELATER###
