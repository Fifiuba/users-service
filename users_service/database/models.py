from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer
from sqlalchemy.ext.declarative import declarative_base
from .database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("user_name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    phone_number = Column("phone_number", String(255), nullable=True)
    age = Column("age", Integer, nullable=True)
    tokenId = Column("tokenId", String(255), nullable=True)


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    default_address = Column("default_address", String(255), nullable=True)


class Driver(Base):
    __tablename__ = "drivers"

    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    license_plate = Column("license_plate", String(255), nullable=True)
    car_model = Column("car_model", String(255), nullable=True)


class GoogleUser(Base):
    __tablename__ = "googleUser"

    userId = Column("userId", Integer, ForeignKey("users.id"), nullable=False)
    googleId = Column(
        "googleId", Integer, primary_key=True
    )  # TODO: ver si es integer o string el google id


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
