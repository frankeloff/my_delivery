from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Order(Base):

    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    status = Column(String)
    price = Column(Integer)
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    chef_id = Column(Integer, ForeignKey("chef.chef_id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier.supplier_id"), nullable=False)
    products = relationship("Products", secondary="order_details", lazy="selectin")
    chef = relationship("Chef", lazy="selectin", uselist=False)
    supplier = relationship("Supplier", lazy="selectin", uselist=False)


class OrderDetails(Base):
    __tablename__ = "order_details"
    product_id = Column(
        Integer, ForeignKey("products.product_id"), nullable=False, primary_key=True
    )
    order_id = Column(
        Integer, ForeignKey("orders.order_id"), nullable=False, primary_key=True
    )
    quantity = Column(Integer, nullable=False)
