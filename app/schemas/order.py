from typing import List

from pydantic import BaseModel


class BaseOrder(BaseModel):
    chef_name: str
    supplier_name: str
    price: int


class Order(BaseOrder):
    pass


class BaseGetOrder(BaseOrder):
    product_names: List[str]
    status: str


class GetOrder(BaseModel):
    order_list: List[BaseGetOrder]
    total_price: int

    class Config:
        orm_mode = True


class OrderForStaff(BaseModel):
    order_id: int
    products: List[str]

    class Config:
        orm_mode = True
