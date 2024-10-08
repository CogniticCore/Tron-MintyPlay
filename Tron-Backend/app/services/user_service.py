from datetime import datetime

from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from ..schemas import user_schema
from ..schemas.user_schema import UserCreate, DatabaseUserCreate, UserResponse
from ..core.database import user_collection
from ..utils.helper.user_helper import hash_password
from ..models.user_model import serialize

from datetime import datetime

async def register(request: user_schema.UserCreate):
    # Check if email already exists
    existing_email = await user_collection.find_one({"email": request.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered."
        )
    
    existing_username = await user_collection.find_one({"username": request.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already registered."
        )
    
    current_time = datetime.now()
    
    hashed_password = hash_password(request.password)

    user_data = DatabaseUserCreate(
        username=request.username,
        email=request.email,
        password=hashed_password,
        bio=None,
        nfts=[],
        achievements=[],
        is_active=True,
        date_joined=current_time,
        games=[]
    )

    user_data_dict = user_data.model_dump()

    result = await user_collection.insert_one(user_data_dict)
    new_user_id = str(result.inserted_id)

    return UserResponse(
        user_id=new_user_id,
        username=request.username,
        email=request.email,
        bio=None,
        nfts=[],
        achievements=[],
        is_active=True,
        date_joined=current_time,
        games=[]
    )

async def all_user():
    """
    Service function to retrieve all user data from the database.
    
    Args:
        None

    Returns:
        list[dict]: User data if found.
    """
    query = {}
    cursor = user_collection.find(query)

    users = []
    async for user in cursor:  # Process the cursor asynchronously
        users.append(serialize(user))

    if users:
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found in the database."
        )