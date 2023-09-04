from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from core.models.user import User
from core.schemas.token import TokenBase
from core.schemas.user import UserRead, UserCreate
from v1.functions.auth import authenticate_user, create_access_token, get_password_hash, get_current_user

from config.connection import get_db
from v1.functions.crud import create_

router = APIRouter()


@router.post("/token", response_model=TokenBase)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/", response_model=UserRead)
def register(new_row: UserCreate, db: Session = Depends(get_db)):
    new_row.password = get_password_hash(new_row.password)
    existing = db.query(User).filter((User.login == new_row.login) | (User.email == new_row.email)).all()
    if existing:
        raise HTTPException(status_code=409, detail="Login or email taken")
    return create_(User, new_row, db)



