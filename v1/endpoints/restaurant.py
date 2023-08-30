from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.schemas.restaurant import RestaurantBase, RestaurantCreate, RestaurantRead
from core.models.restaurant import Restaurant
from core.schemas.user import UserRead
from v1.functions.auth import get_current_user
from v1.functions.crud import get_all_, get_one_, create_, update_, delete_
from config.connection import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/", response_model=List[RestaurantRead])
def get_all(db: Session = Depends(get_db)):
    return get_all_(Restaurant, db)


@router.get("/{item_id}", response_model=RestaurantRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    department = get_one_(Restaurant, item_id, db)
    if department is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return department


@router.post("/", response_model=RestaurantRead)
def create(new_row: RestaurantCreate, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    new_row.user_id = current_user.id
    row = create_(Restaurant, new_row, db)
    return row


@router.put("/{item_id}", response_model=RestaurantRead)
def update(item_id: int, row_new: RestaurantBase, db: Session = Depends(get_db)):
    row = update_(Restaurant, row_new, item_id, db)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return row


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    if delete_(Restaurant, item_id, db) is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return {"ok": True}
