from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.schemas.restaurant import RestaurantBase, RestaurantUpdate, RestaurantRead, RestaurantCreate
from core.models.restaurant import Restaurant
from core.schemas.user import UserRead
from v1.functions.auth import get_current_user
from v1.functions.crud import get_all_, get_one_, create_, update_, delete_
from config.connection import SessionLocal, get_db

router = APIRouter()


@router.get("/", response_model=List[RestaurantRead])
def get_my(get_not_my_public: bool = False, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    user_id = current_user.id
    if current_user.is_admin:
        cafes = get_all_(Restaurant, db)
    else:
        if get_not_my_public:
            cafes = db.query(Restaurant).filter(
                or_(
                    Restaurant.user_id.like(user_id),
                    Restaurant.is_public.is_(True)
                )
            )
        else:
            cafes = db.query(Restaurant).filter_by(user_id=user_id)
    return cafes


@router.get("/{item_id}", response_model=RestaurantRead)
def get_one(item_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    cafe = get_one_(Restaurant, item_id, db)
    if cafe is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    if current_user.id == cafe.user_id or current_user.is_admin or cafe.is_public == True:
        return cafe

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.post("/", response_model=RestaurantRead)
def create(new_row: RestaurantCreate, db: Session = Depends(get_db),
           current_user: UserRead = Depends(get_current_user)):
    existing = db.query(Restaurant).filter(
        (Restaurant.user_id == current_user.id) & (Restaurant.name == new_row.name)).all()
    if existing:
        raise HTTPException(status_code=409, detail="Already created")
    if not current_user.is_admin:
        new_row.is_public = False
    new_row = RestaurantCreate(**dict(new_row))
    new_row.user_id = current_user.id
    row = create_(Restaurant, new_row, db)
    return row


@router.put("/{item_id}", response_model=RestaurantRead)
def update(item_id: int, row_new: RestaurantUpdate, db: Session = Depends(get_db),
           current_user: UserRead = Depends(get_current_user)):
    cafe = db.get(Restaurant, item_id)
    row = None
    if cafe is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    if not current_user.is_admin:
        row_new.is_public = False
    if current_user.id == cafe.user_id or current_user.is_admin:
        row = update_(Restaurant, row_new, item_id, db, row=cafe)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return row


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    cafe = db.get(Restaurant, item_id)
    if cafe is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    if current_user.id != cafe.user_id and current_user.is_admin is not True:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    db.delete(cafe)
    db.commit()
    return {"ok": True}
