import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models.user import User


class Client(User):

    __tablename__ = "client"

    client_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "client",
    }
