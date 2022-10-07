from typing import Dict, List

from pydantic import BaseModel


class BaseOrder(BaseModel):
    chef_name: str
    supplier_name: str
    price: int


class Order(BaseOrder):
    pass


class ProductQuantity(BaseModel):
    product: str
    quantity: int


class GetOrder(BaseModel):
    order_id: int
    order_list: List[ProductQuantity]
    total_price: int

    class Config:
        orm_mode = True


class OrderForStaff(BaseModel):
    order_id: int
    product_list: List[ProductQuantity]

    class Config:
        orm_mode = True
