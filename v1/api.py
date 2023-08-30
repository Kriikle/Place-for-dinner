from fastapi import APIRouter, Depends
from v1.endpoints import auth
from v1.endpoints import user, docs, restaurant
from v1.functions.auth import get_current_user

router = APIRouter()

api_router = APIRouter()
api_router.include_router(docs.router, tags=["docs"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)])
api_router.include_router(
    restaurant.router,
    prefix="/restaurants",
    tags=["restaurants"],
    dependencies=[Depends(get_current_user)])

