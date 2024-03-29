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


class UserUpdate(UserBase):
    login: Optional[constr(max_length=120)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(max_length=120)] = None


class UserCreateAdmin(UserBase):
    password: constr(max_length=120)
    is_admin: bool


class UserUpdateAdmin(UserBase):
    login: Optional[constr(max_length=120)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(max_length=120)] = None
    is_admin: Optional[bool] = None


class UserRead(UserBase):
    pass
