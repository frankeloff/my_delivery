import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from . import Base


class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    position = Column(String(length=10))
    password = Column(String(60))
    created_at = Column(DateTime(True), default=datetime.datetime.now)
    updated_at = Column(DateTime(True), default=datetime.datetime.now)

    __mapper_args__ = {
        "polymorphic_on": position,
    }
