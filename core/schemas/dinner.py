from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr


class DinnerBase(BaseModel):
    restaurant_id: int

    class Config:
        from_attributes = True


class DinnerCreate(DinnerBase):
    user_id: Optional[int] = None


class DinnerRead(DinnerBase):
    id: int
    date_created: datetime

