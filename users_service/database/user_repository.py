from typing import Union
from sqlalchemy.orm import Session
from . import crud, schema, exceptions
from users_service.utils import token_handler, password_handler


def get_user_by_email(email: str, db: Session):
    user = crud.get_user_by_email(email, db)
    if not user:
        raise exceptions.UserNotFoundError
    return user


def get_users(db):
    return crud.get_users(db)


def create_user(token_id: Union[str, None], user: schema.UserBase, db: Session):
    if user.user_type == "passenger":
        user_create = crud.create_passenger(token_id, user, db)
    else:
        user_create = crud.create_driver(token_id, user, db)
    return user_create


def edit_user_info(user_id, user: schema.UserPatch, db: Session):
    if user.user_type == "passenger":
        db_user, passenger = crud.edit_passenger_info(
            user_id, user.fields[0], user.fields[1], db
        )
        db_user.user_type = user.user_type
        return db_user, passenger
    else:
        db_user, driver = crud.edit_driver_info(
            user_id, user.fields[0], user.fields[1], db
        )
        db_user.user_type = user.user_type

        return db_user, driver


def user_profile(user_id: int, user_type: str, db: Session):
    if user_type == "passenger":
        passenger = crud.get_passenger_by_id(user_id, db)
        if not passenger:
            raise exceptions.PassengerNotFoundError
        user = crud.get_user_by_id(user_id, db)
        return user, passenger
    else:
        driver = crud.get_driver_by_id(user_id, db)
        if not driver:
            raise exceptions.DriverNotFoundError
        user = crud.get_user_by_id(user_id, db)
        return user, driver


def add_user_info(user_id: int, user: schema.UserPatch, db: Session):

    if user.user_type == "passenger":
        passenger = crud.add_passenger_address(
            user_id, user.fields[0]["default_address"], db
        )
        return passenger
    else:
        driver = crud.add_driver_car_info(
            user_id,
            user.fields[0]["license_plate"],
            user.fields[0]["car_model"],
            db,
        )
        return driver


def verified_user(email:str , db: Session):
    db_user = crud.get_user_by_email(email, db)
    return db_user


def login(email, token_id, db: Session):

    db_user = verified_user(email, db)
    if db_user is None:
        raise exceptions.UserWrongLoginInformation
    if not token_id == db_user.tokenId:
        raise exceptions.UserWrongLoginInformation

    token = token_handler.create_access_token(db_user.id, True)
    return token


def login_google(googleUser: schema.GoogleLogin, db: Session):
    user_id = crud.login_google(googleUser, db)
    token = token_handler.create_access_token(user_id, True)
    return token


def delete_user(user_id, user_type, db: Session):
    if user_type == "passenger":
        crud.delete_passenger(user_id, db)
        return user_id
    else:
        crud.delete_driver(user_id, db)
        return user_id


def get_user_by_id(user_id: int, db: Session):
    user = crud.get_user_by_id(user_id, db)
    if not user:
        raise exceptions.UserNotFoundError
    return user
