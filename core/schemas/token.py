from typing import List, Optional
from pydantic import BaseModel, constr


class TokenBase(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str = None
