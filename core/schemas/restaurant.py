from pydantic import BaseModel, constr, PositiveFloat


class RestaurantBase(BaseModel):
    id: int
    name: constr(max_length=120)
    img_path: constr(max_length=120)
    address: constr(max_length=120)
    lat: float
    lot: float

    class Config:
        from_attributes = True


class RestaurantCreate(RestaurantBase):
    user_id: int


class RestaurantRead(RestaurantBase):
    user_id: int
