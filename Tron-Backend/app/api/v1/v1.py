from fastapi import APIRouter
from .endpoints import games, bounties, users, nfts, orderitem, purchases

router = APIRouter(
    prefix='/v1',
    # tags=['v1']
)

router.include_router(users.router)
router.include_router(games.router)
router.include_router(bounties.router)
router.include_router(nfts.router)
router.include_router(orderitem.router)
router.include_router(purchases.router)