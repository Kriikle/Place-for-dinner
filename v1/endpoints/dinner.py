from random import choice
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from config.connection import SessionLocal, get_db
from core.models.dinner import Dinner
from core.models.restaurant import Restaurant
from core.schemas.dinner import DinnerRead, DinnerCreate, DinnerBase
from core.schemas.restaurant import RestaurantRead

from core.schemas.user import UserRead
from v1.functions.auth import get_current_user
from v1.functions.crud import get_all_, get_one_, create_

router = APIRouter()


@router.get("/visit", response_model=RestaurantRead)  #
async def dinner_to_visit(
        only_my_cafes: bool = True,
        auto_add: bool = False,
        history_check_limit: int = 3,
        radius: int = 0,
        my_lat: float = 0,
        my_lot: float = 0,
        db: Session = Depends(get_db),
        current_user: UserRead = Depends(get_current_user)):
    user_id = current_user.id
    if not only_my_cafes:
        cafes = db.query(Restaurant).filter(
            or_(
                Restaurant.user_id.like(user_id),
                Restaurant.is_public.is_(True)
            )
        )
    else:
        cafes = db.query(Restaurant).filter(Restaurant.is_public.is_(True))
    if cafes.first():
        cafe = choice(cafes.all())
    else:
        raise HTTPException(status_code=404, detail=f"Cafes not found")
    if auto_add:
        new_row = DinnerCreate(
            user_id=current_user.id,
            restaurant_id=cafe.id,
        )
        row = create_(Dinner, new_row, db)
    return cafe


@router.post("/add_visit", response_model=DinnerRead)
def add_visit(new_row: DinnerBase, db: Session = Depends(get_db),
              current_user: UserRead = Depends(get_current_user)):
    new_row = DinnerCreate(**dict(new_row))
    new_row.user_id = current_user.id
    row = create_(Dinner, new_row, db)
    return row


@router.get("/", response_model=List[DinnerRead])
async def dinners_me(db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    user_id = current_user.id
    if current_user.is_admin:
        dinners = get_all_(Dinner, db)
    else:
        dinners = db.query(Dinner).filter(Dinner.user_id.like(user_id))
    return dinners


@router.get("/{item_id}", response_model=DinnerRead)
def get_one(item_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    dinner = get_one_(Dinner, item_id, db)
    if dinner is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    if current_user.id == dinner.user_id or current_user.is_admin:
        return dinner
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    dinner = db.get(Dinner, item_id)
    if dinner is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    if current_user.id != dinner.user_id and current_user.is_admin is not True:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    db.delete(dinner)
    db.commit()
    return {"ok": True}
