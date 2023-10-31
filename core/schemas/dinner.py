from datetime import datetime

from pydantic import BaseModel, constr


class DinnerBase(BaseModel):
    user_id: int
    restaurant_id: int

    class Config:
        from_attributes = True


class DinnerCreate(DinnerBase):
    pass


class DinnerRead(DinnerBase):
    id: int
    date_created: datetime

