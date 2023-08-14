from pydantic import BaseModel, constr


class RestaurantBase(BaseModel):
    name: constr(max_length=120)
    img_path: constr(max_length=120)
    address: constr(max_length=120)

    class Config:
        from_attributes = True


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantRead(RestaurantBase):
    id: int
