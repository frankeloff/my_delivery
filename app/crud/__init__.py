from .chef import chef_crud
from .client import client_crud
from .orders import orders_crud
from .products import products_crud
from .supplier import supplier_crud
from .user import user_crud

__all__ = [
    "chef_crud",
    "client_crud",
    "supplier_crud",
    "user_crud",
    "products_crud",
    "orders_crud",
]
