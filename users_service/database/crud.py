from typing import Union
from users_service.utils import password_handler
from . import models, schema, exceptions
from sqlalchemy.orm import Session


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
    hashed_password = password_handler.get_hashed_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        phone_number=user.phone_number,
        age=user.age,
        tokenId=token_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.user_type = user.user_type
    return db_user, False


def create_passenger_with_id(user_id: int, db: Session):
    db_passenger = models.Passenger(id=user_id, default_address=None)
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)


def create_driver_with_id(user_id: int, db: Session):
    db_driver = models.Driver(id=user_id, license_plate=None, car_model=None)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)


def create_passenger(token_id: Union[str, None], user: schema.UserBase, db: Session):
    db_user, already_existing_user = create_user(token_id, user, db)
    if already_existing_user and (
        get_driver_by_id(db_user.id, db) is None
        or get_passenger_by_id(db_user.id, db) is not None
    ):
        raise exceptions.PassengerAlreadyExists
    else:
        create_passenger_with_id(db_user.id, db)
    return db_user


def create_driver(token_id: Union[str, None], user: schema.UserBase, db: Session):

    db_user, already_existing_user = create_user(token_id, user, db)
    if already_existing_user and (
        get_passenger_by_id(db_user.id, db) is None
        or get_driver_by_id(db_user.id, db) is not None
    ):
        raise exceptions.DriverAlreadyExists
    else:
        create_driver_with_id(db_user.id, db)
    return db_user


def add_passenger_address(passenger_id: int, default_address: str, db: Session):
    db_passenger = get_passenger_by_id(passenger_id, db)
    if db_passenger is None:
        raise exceptions.PassengerNotFoundError
    db_passenger.default_address = default_address
    db.commit()
    db.refresh(db_passenger)
    return db_passenger


def add_driver_car_info(
    driver_id: int, license_plate: str, car_model: str, db: Session
):
    db_driver = get_driver_by_id(driver_id, db)
    if db_driver is None:
        raise exceptions.DriverNotFoundError
    db_driver.license_plate = license_plate
    db_driver.car_model = car_model
    db.commit()
    db.refresh(db_driver)
    return db_driver


def login_google(googleUser: schema.GoogleLogin, db: Session):
    # caso 1 email no esta en la tabla de relacion google usuairo
    relationship = (
        db.query(models.GoogleUser)
        .filter(models.GoogleUser.googleId == googleUser.googleId)
        .first()
    )
    if not relationship:
        # hay algun usuario con ese email:
        user = get_user_by_email(googleUser.email, db)
        if user:
            raise exceptions.UserAlreadyExists
        else:
            user_aux = schema.UserBase(
                user_type="",
                name=googleUser.name,
                password="",
                phone_number=None,
                email=googleUser.email,
                age=None,
            )
            user, _ = create_user(user_aux, db)
            db_google_user = models.GoogleUser(
                userId=user.id, googleId=googleUser.googleId
            )
            db.add(db_google_user)
            db.commit()
            return user.name

    user = get_user_by_id(relationship.userId, db)
    return user.id


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
        raise exceptions.PassengerNotFoundError
    user = edit_user(user_id, userInfo, db)
    attribute_passenger = removeNoneValues(passengerInfo)
    for attr, value in attribute_passenger.items():
        setattr(passenger, attr, value)

    db.commit()
    db.refresh(user)
    db.refresh(passenger)
    return user, passenger


def edit_driver_info(
    user_id: int,
    userInfo: schema.UserEditFields,
    driverInfo: schema.DriverEditFields,
    db: Session,
):
    driver = get_driver_by_id(user_id, db)
    if not driver:
        raise exceptions.DriverNotFoundError
    user = edit_user(user_id, userInfo, db)

    attribute_passenger = removeNoneValues(driverInfo)
    for attr, value in attribute_passenger.items():
        setattr(driver, attr, value)
    db.commit()
    db.refresh(user)
    db.refresh(driver)
    return user, driver


def delete_passenger(user_id, db):
    passenger = get_passenger_by_id(user_id, db)
    if not passenger:
        raise exceptions.PassengerNotFoundError
    user = get_user_by_id(user_id, db)
    db.delete(passenger)
    db.delete(user)
    db.commit()


def delete_driver(user_id, db):
    driver = get_driver_by_id(user_id, db)
    if not driver:
        raise exceptions.DriverNotFoundError
    user = get_user_by_id(user_id, db)
    db.delete(driver)
    db.delete(user)
    db.commit()
