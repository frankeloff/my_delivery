import datetime

from pydantic import BaseModel, EmailStr, constr


class BaseClient(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ClientIn(BaseClient):
    password: constr(min_length=10)

    class Config:
        orm_mode = True


class ClientOut(BaseClient):
    client_id: int

    class Config:
        orm_mode = True
