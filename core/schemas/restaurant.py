from typing import Optional

from pydantic import BaseModel, constr, PositiveFloat, Field


class RestaurantBase(BaseModel):
    name: constr(max_length=120)
    img_path: Optional[constr(max_length=120)] = None
    address: Optional[constr(max_length=120)] = None
    lat: Optional[PositiveFloat] = None
    lot: Optional[PositiveFloat] = None
    is_public: Optional[bool] = False

    class Config:
        from_attributes = True


class RestaurantCreate(RestaurantBase):
    user_id: Optional[int] = None


class RestaurantUpdate(RestaurantBase):
    name: Optional[constr(max_length=120)] = None
    img_path: Optional[constr(max_length=120)] = None
    address: Optional[constr(max_length=120)] = None


class RestaurantRead(RestaurantBase):
    id: int
