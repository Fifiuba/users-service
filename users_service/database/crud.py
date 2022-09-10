from . import models, schema, exceptions
from sqlalchemy.orm import Session
from .database import SessionLocal

# TODO: Modular el hasher
from passlib.context import CryptContext

# from fastapi import Depends


# Dependency
def get_db():
    db = SessionLocal()()
    try:
        yield db
    finally:
        db.close()


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def get_users(db: Session):
    query_response = db.query(models.User).all()
    return query_response


def get_user_by_name(name: str, db: Session):
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_by_id(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_passenger_by_id(passenger_id: int, db: Session):
    return (
        db.query(models.Passenger).filter(models.Passenger.id == passenger_id).first()
    )


def get_driver_by_id(driver_id: int, db: Session):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()


def user_exists(username, db: Session):
    return get_user_by_name(username, db) is not None


def create_user(user: schema.UserBase, db: Session):
    if user_exists(user.name, db):
        raise exceptions.UserAlreadyExists
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(
        name=user.name,
        password=hashed_password,
        phone_number=user.phone_number,
        age=user.age,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_passenger(id_user: int, db: Session):
    db_passenger = models.Passenger(id=id_user, default_address=None)
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)


def create_driver(id_user: int, db: Session):
    db_driver = models.Driver(id=id_user, license_plate=None, car_model=None)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)


def add_passenger_address(passenger: schema.PassengerBase, db: Session):
    db_passenger = get_passenger_by_id(passenger.id, db)
    if db_passenger is None:
        raise exceptions.PassengerNotFoundError
    db_passenger.default_address = passenger.default_address
    db.commit()
    db.refresh(db_passenger)
    return db_passenger


def add_driver_car_info(driver: schema.DriverBase, db: Session):
    db_driver = get_driver_by_id(driver.id, db)
    if db_driver is None:
        raise exceptions.DriverNotFoundError
    db_driver.license_plate = driver.license_plate
    db_driver.car_model = driver.car_model
    db.commit()
    db.refresh(db_driver)
    return db_driver
