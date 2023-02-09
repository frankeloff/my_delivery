from sqlalchemy import Column, Integer, String

from . import Base


class Products(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Integer)
