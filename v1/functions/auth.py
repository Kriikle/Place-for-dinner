from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config.connection import get_db
from core.models.user import User
from core.schemas.token import TokenData
from config.params import TOKEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter_by(login=username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN['ACCESS_TOKEN_EXPIRE_MINUTES'])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN['SECRET_KEY'], algorithm=TOKEN['ALGORITHM'])
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, TOKEN['SECRET_KEY'], algorithms=TOKEN['ALGORITHM'])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter_by(login=token_data.login).first()
    if user is None:
        raise credentials_exception
    return user


