from typing import Optional

from pydantic import BaseModel, constr, PositiveFloat, Field


class RestaurantBase(BaseModel):
    name: constr(max_length=120)
    img_path: Optional[constr(max_length=120)] = None
    address: Optional[constr(max_length=120)] = None
    lat: Optional[float] = None
    lot: Optional[float] = None
    is_public: bool

    class Config:
        from_attributes = True


class RestaurantCreate(RestaurantBase):
    user_id: Optional[int] = None


class RestaurantUpdate(RestaurantBase):
    name: Optional[constr(max_length=120)]
    img_path: Optional[constr(max_length=120)]
    address: Optional[constr(max_length=120)]
    lat: Optional[float]
    lot: Optional[float]
    is_public: bool


class RestaurantRead(RestaurantBase):
    id: int
