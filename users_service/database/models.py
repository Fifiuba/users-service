from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("user_name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    phone_number = Column("phone_number", String(255), nullable=True)
    age = Column("age", Integer, nullable=True)
    picture = Column("picture", String(255), nullable=True)
    tokenId = Column("tokenId", String(255), nullable=True)


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    default_address = Column("default_address", String(255), nullable=True)
    score = Column("score", Integer, nullable=True)


class Driver(Base):
    __tablename__ = "drivers"

    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    license_plate = Column("license_plate", String(255), nullable=True)
    car_model = Column("car_model", String(255), nullable=True)
    vip = Column("vip", Boolean, unique=False, default=False)
    score = Column("score", Integer, nullable=True)


class GoogleUser(Base):
    __tablename__ = "googleUser"

    userId = Column("userId", Integer, ForeignKey("users.id"), nullable=False)
    googleId = Column("googleId", String(255), primary_key=True)

class PassengerScores(Base):
    __tablename__ = "passengersScores"
    scoreid = Column("id", Integer, primary_key=True, autoincrement=True)
    userId = Column("userId", Integer, ForeignKey("passengers.id"), nullable=False)
    rating = Column("score", Integer, nullable=True)

class DriverScores(Base):
    __tablename__ = "DriversScores"
    scoreid = Column("id", Integer, primary_key=True, autoincrement=True)
    userId = Column("userId", Integer, ForeignKey("drivers.id"), nullable=False)
    rating = Column("score", Integer, nullable=True)

