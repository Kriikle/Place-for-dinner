from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.schemas.user import UserRead, UserCreateAdmin, UserUpdateAdmin
from core.models.user import User
from v1.functions.crud import get_all_, get_one_, create_, update_, delete_
from v1.functions.auth import get_password_hash

from config.connection import get_db

router = APIRouter()


@router.get("/", response_model=List[UserRead])
def get_all(db: Session = Depends(get_db)):
    return get_all_(User, db)


@router.get("/{item_id}", response_model=UserRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    row = get_one_(User, item_id, db)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return row


@router.post("/", response_model=UserRead)
def create(new_row: UserCreateAdmin, db: Session = Depends(get_db)):
    new_row.password = get_password_hash(new_row.password)
    existing = db.query(User).filter((User.login == new_row.login) | (User.email == new_row.email)).all()
    if existing:
        raise HTTPException(status_code=409, detail="Login or email taken")
    return create_(User, new_row, db)


@router.put("/{item_id}", response_model=UserRead)
def update(item_id: int, new_row: UserUpdateAdmin, db: Session = Depends(get_db)):
    row = update_(User, new_row, item_id, db)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return row


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    if delete_(User, item_id, db) is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return {"ok": True}


