from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer
from .database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("user_name", String(255), nullable=False)
    password = Column("password", String(255), nullable=False)
    phone_number = Column("phone_number", String(255), nullable=True)
    age = Column("age", Integer, nullable=True)


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    default_address = Column("default_address", String(255), nullable=True)


class Driver(Base):
    __tablename__ = "drivers"

    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    license_plate = Column("license_plate", String(255), nullable=True)
    car_model = Column("car_model", String(255), nullable=True)

