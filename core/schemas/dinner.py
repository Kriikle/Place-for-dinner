from pydantic import BaseModel, constr


class DinnerBase(BaseModel):
    name: constr(max_length=120)
    user_id: int
    lot: int

    class Config:
        from_attributes = True


class DinnerCreate(DinnerBase):
    pass


class DinnerRead(DinnerBase):
    id: int
    datetime: int
    user_id: int
    restaurant_id: int
