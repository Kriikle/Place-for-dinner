from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from core.schemas.token import TokenBase
from v1.functions.auth import authenticate_user, create_access_token

from config.connection import get_db

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
