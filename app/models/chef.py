from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.user import User


class Chef(User):
    __tablename__ = "chef"

    chef_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    number_of_orders = Column(Integer, default=0)

    __mapper_args__ = {
        "polymorphic_identity": "chef",
    }
