from typing import Union
from . import models, schema, exceptions
from sqlalchemy.orm import Session
import json_log_formatter
import logging

formatter = json_log_formatter.JSONFormatter()

json_handler = logging.FileHandler(filename='./logs.log')
json_handler.setFormatter(formatter)

logger = logging.getLogger('users_service_logger')
logger.addHandler(json_handler)
logger.setLevel(logging.DEBUG)

def get_passengers(db: Session):
    passengers = db.query(models.User).join(models.Passenger).all()
    return passengers


def get_drivers(db: Session):
    drivers = (
        db.query(
            models.User,
        )
        .join(models.Driver)
        .all()
    )
    return drivers


def get_users(db: Session):
    query_response = db.query(models.User).all()
    return query_response


def get_user_by_name(name: str, db: Session):
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_passenger_by_id(passenger_id: int, db: Session):
    return (
        db.query(models.Passenger).filter(models.Passenger.id == passenger_id).first()
    )


def get_driver_by_id(driver_id: int, db: Session):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()


def user_exists(username, db: Session):
    user = get_user_by_name(username, db)
    return user


def create_user(token_id: Union[str, None], user: schema.UserBase, db: Session):
    user_aux = get_user_by_email(user.email, db)

    if user_aux:
        user_aux.user_type = user.user_type
        return user_aux, True
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        age=user.age,
        picture=user.picture,
        tokenId=token_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.user_type = user.user_type
    return db_user, False


def create_passenger_with_id(user_id: int, db: Session):
    db_passenger = models.Passenger(id=user_id, default_address=None, score=3)
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)


def create_driver_with_id(user_id: int, db: Session):
    db_driver = models.Driver(id=user_id, license_plate=None, car_model=None, score=3)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)


def create_passenger(token_id: Union[str, None], user: schema.UserBase, db: Session):
    db_user, already_existing_user = create_user(token_id, user, db)
    if already_existing_user and (
        get_driver_by_id(db_user.id, db) is None
        or get_passenger_by_id(db_user.id, db) is not None
    ):
        logger.warning("Passenger with id %d already exists", db_user.id, extra={'type': 'WARN', 
                                                        'endpoint': '/users',
                                                         'method': 'POST', 
                                                         'operation': 'Register',
                                                         'status': 401})
        raise exceptions.PassengerAlreadyExists
    else:
        create_passenger_with_id(db_user.id, db)
    logger.debug("Create passenger %d with email %s", db_user.id, db_user.email, extra= {'type': 'DEBUG', 
                                                        'endpoint': '/users',
                                                         'method': 'POST', 
                                                         'operation': 'Register',
                                                         'status': 200})
    return db_user


def create_driver(token_id: Union[str, None], user: schema.UserBase, db: Session):

    db_user, already_existing_user = create_user(token_id, user, db)
    if already_existing_user and (
        get_passenger_by_id(db_user.id, db) is None
        or get_driver_by_id(db_user.id, db) is not None
    ):  
        logger.warning("Driver with id %d already exists", db_user.id, extra={'type': 'WARN', 
                                                        'endpoint': '/users',
                                                         'method': 'POST', 
                                                         'operation': 'Register',
                                                         'status': 401})
        raise exceptions.DriverAlreadyExists
    else:
        create_driver_with_id(db_user.id, db)
    logger.debug("Create driver %d with email %s", db_user.id, db_user.email, extra= {'type': 'DEBUG', 
                                                        'endpoint': '/users',
                                                         'method': 'POST', 
                                                         'operation': 'Register',
                                                         'status': 200})
    logger.info("Driver created")
    return db_user


def add_passenger_address(passenger_id: int, default_address: str, db: Session):
    db_passenger = get_passenger_by_id(passenger_id, db)
    if db_passenger is None:
        logger.warning("Passenger %d not found", passenger_id, extra={'type': 'WARN', 
                                                        'endpoint': '/users/',
                                                         'method': 'PATCH', 
                                                         'operation': 'add user info',
                                                         'status': 404})
        raise exceptions.PassengerNotFoundError
    db_passenger.default_address = default_address
    db.commit()
    db.refresh(db_passenger)
    logger.debug("Updated passenger %d", db_passenger.id, extra= {'type': 'DEBUG', 
                                                        'endpoint': '/users/',
                                                         'method': 'PATCH', 
                                                         'operation': 'add user info',
                                                         'status': 200})
    logger.info("Passenger updated")
    return db_passenger


def add_driver_car_info(
    driver_id: int, license_plate: str, car_model: str, db: Session
):
    db_driver = get_driver_by_id(driver_id, db)
    if db_driver is None:
        logger.warning("Driver %d not found", driver_id,extra= {'type': 'WARN', 
                                                        'endpoint': '/users/',
                                                         'method': 'PATCH', 
                                                         'operation': 'add user info',
                                                         'status': 404})
        raise exceptions.DriverNotFoundError
    db_driver.license_plate = license_plate
    db_driver.car_model = car_model
    db.commit()
    db.refresh(db_driver)
    logger.debug("Updated driver %d", db_driver.id,  extra={'type': 'DEBUG', 
                                                        'endpoint': '/users/',
                                                         'method': 'PATCH', 
                                                         'operation': 'add user info',
                                                         'status': 200})
    logger.info("Driver updated")
    return db_driver


def get_google_relationship(uid: str, db: Session):
    return db.query(models.GoogleUser).filter(models.GoogleUser.googleId == uid).first()


def create_google_relationship(uid: str, id: int, db: Session):
    db_google_user = models.GoogleUser(userId=id, googleId=uid)
    db.add(db_google_user)
    db.commit()
    logger.debug("Create google user %s", uid)
    logger.info("Create google user", extra= {'type': 'INFO', 
                                            'endpoint': '/users/loginGoogle',
                                            'method': 'POST', 
                                            'operation': 'register',
                                            'status': 200})


def removeNoneValues(dict_aux: dict):
    dict_aux2 = {}
    for key, value in dict_aux.items():
        if value is not None:
            dict_aux2[key] = value
    return dict_aux2


def edit_user(user_id: int, userInfo: schema.UserEditFields, db: Session):
    user = get_user_by_id(user_id, db)
    attributes_user = removeNoneValues(userInfo)
    for attr, value in attributes_user.items():
        setattr(user, attr, value)
    db.commit()
    db.refresh(user)
    return user


def edit_passenger_info(
    user_id: int,
    userInfo: schema.UserEditFields,
    passengerInfo: schema.PassengerEditFields,
    db: Session,
):
    passenger = get_passenger_by_id(user_id, db)
    if not passenger:
        logger.warning("Passenger %d not found", user_id,extra={'type': 'WARN', 
                                                        'endpoint': '/users/me',
                                                         'method': 'PATCH', 
                                                         'operation': 'update user info',
                                                         'status': 404})
        raise exceptions.PassengerNotFoundError
    user = edit_user(user_id, userInfo, db)
    attribute_passenger = removeNoneValues(passengerInfo)
    for attr, value in attribute_passenger.items():
        setattr(passenger, attr, value)

    db.commit()
    db.refresh(user)
    db.refresh(passenger)
    logger.debug("Updated passenger %d info", passenger.id,extra= {'type': 'DEBUF', 
                                                        'endpoint': '/users/me',
                                                         'method': 'PATCH', 
                                                         'operation': 'update user info',
                                                         'status': 200})
    logger.info("Passenger updated")
    return user, passenger


def edit_driver_info(
    user_id: int,
    userInfo: schema.UserEditFields,
    driverInfo: schema.DriverEditFields,
    db: Session,
):
    driver = get_driver_by_id(user_id, db)
    if not driver:
        logger.warning("Driver %d not found", user_id,extra= {'type': 'WARN', 
                                                        'endpoint': '/users/me',
                                                         'method': 'PATCH', 
                                                         'operation': 'update user info',
                                                         'status': 404})
        raise exceptions.DriverNotFoundError
    user = edit_user(user_id, userInfo, db)

    attribute_passenger = removeNoneValues(driverInfo)
    for attr, value in attribute_passenger.items():
        setattr(driver, attr, value)
    db.commit()
    db.refresh(user)
    db.refresh(driver)
    logger.debug("Updated driver %d info", driver.id, extra={'type': 'INFO', 
                                                        'endpoint': '/users/me',
                                                         'method': 'PATCH', 
                                                         'operation': 'update user info',
                                                         'status': 200})
    logger.info("Driver updated")
    return user, driver


def delete_passenger(user_id, db):
    passenger = get_passenger_by_id(user_id, db)
    if not passenger:
        logger.warning("Passenger %d not found", user_id, extra={'type': 'WARN', 
                                                        'endpoint': '/users/',
                                                         'method': 'DETELE', 
                                                         'operation': 'udelete user',
                                                         'status': 404})
        raise exceptions.PassengerNotFoundError
    user = get_user_by_id(user_id, db)
    db.delete(passenger)
    db.delete(user)
    db.commit()
    logger.debug("Delete passenger %d", passenger.id, extra={'type': 'DEBUG', 
                                                        'endpoint': '/users/',
                                                         'method': 'DELETE', 
                                                         'operation': 'delete user',
                                                         'status': 200})
    logger.info("Passenger deleted")


def delete_driver(user_id, db):
    driver = get_driver_by_id(user_id, db)
    if not driver:
        logger.warning("Driver %d not found", user_id,  extra={'type': 'WARN', 
                                                        'endpoint': '/users/',
                                                         'method': 'DETELE', 
                                                         'operation': 'udelete user',
                                                         'status': 404})
        raise exceptions.DriverNotFoundError
    user = get_user_by_id(user_id, db)
    db.delete(driver)
    db.delete(user)
    db.commit()
    logger.debug("Delete driver %d", driver.id, extra={'type': 'DEBUG', 
                                                        'endpoint': '/users/',
                                                         'method': 'DELETE', 
                                                         'operation': 'delete user',
                                                         'status': 200})
    logger.info("Driver deleted")


def update_score_passenger(passenger: models.Passenger, score: int, db: Session):
    final_score = (passenger.score + score) / 2
    passenger.score = final_score
    db.commit()
    db.refresh(passenger)
    logger.debug("Updated passenger %d score", passenger.id, extra={'type': 'DEBUG', 
                                                        'endpoint': '/users/score',
                                                         'method': 'PATCH', 
                                                         'operation': 'update user score',
                                                         'status': 200})
    logger.info("Passenger updated")
    return passenger


def update_score_driver(driver: models.Driver, score: int, db: Session):
    final_score = (driver.score + score) / 2
    driver.score = final_score
    db.commit()
    db.refresh(driver)
    logger.debug("Updated driver %d score", driver.id, extra={'type': 'DEBUG', 
                                                        'endpoint': '/users/score',
                                                         'method': 'PATCH', 
                                                         'operation': 'update user score',
                                                         'status': 200})
    logger.info("Driver updated")
    return driver
