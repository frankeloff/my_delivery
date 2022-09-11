import datetime

from pydantic import BaseModel, EmailStr, constr


class BaseSupplier(BaseModel):
    first_name: str
    second_name: str
    busy: bool
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SupplierIn(BaseSupplier):
    password: constr(min_length=10)

    class Config:
        orm_mode = True


class SupplierOut(BaseSupplier):
    supplier_id: int

    class Config:
        orm_mode = True
