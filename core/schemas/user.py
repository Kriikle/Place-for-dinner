from typing import List, Optional
from pydantic import BaseModel, constr, EmailStr


class UserBase(BaseModel):
    login: constr(max_length=120)
    email: EmailStr
    firstname: Optional[constr(max_length=120)]
    lastname: Optional[constr(max_length=120)]
    patronymic: Optional[constr(max_length=120)]

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: constr(max_length=120)


class UserRead(UserBase):
    pass

