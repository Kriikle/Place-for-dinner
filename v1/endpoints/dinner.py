from random import choice
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.testing import not_in

from config.connection import SessionLocal, get_db
from core.models.dinner import Dinner
from core.models.restaurant import Restaurant
from core.schemas.dinner import DinnerRead, DinnerCreate, DinnerBase
from core.schemas.restaurant import RestaurantRead

from core.schemas.user import UserRead
from v1.functions.auth import get_current_user
from v1.functions.crud import get_all_, get_one_, create_

router = APIRouter()


@router.get("/visit", response_model=RestaurantRead)
async def dinner_to_visit(
        only_my_cafes: bool = True,
        auto_add: bool = False,
        history_check_limit: Union[int, None] = None,
        radius: Union[int, None] = None,
        my_lat: Union[float, None] = None,
        my_lot: Union[float, None] = None,
        db: Session = Depends(get_db),
        current_user: UserRead = Depends(get_current_user)):
    user_id = current_user.id
    if only_my_cafes:
        query = Restaurant.user_id.like(user_id)
    else:
        query = or_(Restaurant.user_id.like(user_id), Restaurant.is_public.is_(True))
    if history_check_limit:
        if 0 < history_check_limit < 10:
            dinners = db.query(Dinner.restaurant_id).filter(Dinner.user_id.is_(user_id))
            query = and_(
                query,
                Restaurant.id.not_in(
                    [i[0] for i in dinners.order_by(Dinner.date_created.desc()).limit(history_check_limit)]
                )
            )
            #     'select d.restaurant_id from dinner d' +
            #     'WHERE d.user_id =' + str(current_user.id) +
            #     'order by d.date_created' +
            #     'LIMIT ' + str(history_check_limit)))
        else:
            raise HTTPException(status_code=404, detail=f"History_check_limit must be > 0, < 10")

    cafes = db.query(Restaurant).filter(query)
    if cafes.first():
        cafe = choice(cafes.all())
    else:
        raise HTTPException(status_code=404, detail=f"Cafes not found")
    if my_lot and my_lat and radius:
        if my_lot > 0 and my_lat > 0 and 0 < radius < 2000:
            pass
        else:
            pass
    if auto_add:
        new_row = DinnerCreate(
            user_id=current_user.id,
            restaurant_id=cafe.id,
        )
        create_(Dinner, new_row, db)
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
