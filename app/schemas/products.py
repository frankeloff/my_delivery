from typing import Union

from pydantic import BaseModel


class Price(BaseModel):
    price: Union[str, int, None]

    class Config:
        orm_mode = True


class BaseProducts(BaseModel):
    name: str
    price: int


class ProductsOut(BaseProducts):
    class Config:
        orm_mode = True
