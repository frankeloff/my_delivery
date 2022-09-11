from importlib.metadata import metadata

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)

from .chef import Chef
from .client import Client
from .order import Order, OrderDetails
from .product import Products
from .supplier import Supplier
from .user import User

__all__ = [
    "metadata",
    "Chef",
    "Client",
    "Supplier",
    "Products",
    "Order",
    "OrderDetails",
    "User",
]
