import datetime
from typing import List

from pydantic import BaseModel, EmailStr, constr


class BaseChef(BaseModel):
    first_name: str
    second_name: str
    busy: bool
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ChefIn(BaseChef):
    password: constr(min_length=10)

    class Config:
        orm_mode = True


class ChefOut(BaseChef):
    id: int

    class Config:
        orm_mode = True
