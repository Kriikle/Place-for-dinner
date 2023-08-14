from typing import List, Optional
from pydantic import BaseModel, constr, EmailStr


class UserBase(BaseModel):
    login: constr(max_length=120)
    email: EmailStr
    firstname: constr(max_length=120)
    lastname: constr(max_length=120)
    patronymic: constr(max_length=120)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: constr(max_length=120)


class UserRead(UserBase):
    pass

