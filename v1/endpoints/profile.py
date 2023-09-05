from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from core.models.user import User
from core.schemas.token import TokenBase
from core.schemas.user import UserRead, UserCreate, UserBase
from v1.functions.auth import authenticate_user, create_access_token, get_password_hash, get_current_user

from config.connection import get_db
from v1.functions.crud import create_, update_

router = APIRouter()


@router.get("/", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user


@router.put("/", response_model=UserRead)
def update(new_row: UserBase, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    item_id = current_user.id
    row = update_(User, new_row, item_id, db)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return row
