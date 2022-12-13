from typing import Union
from sqlalchemy.orm import Session

from . import crud, schema, exceptions
from users_service.utils import token_handler


def get_user_by_email(email: str, db: Session):
    user = crud.get_user_by_email(email, db)
    if not user:
        raise exceptions.UserNotFoundError
    return user


def get_opinions_users(id: int, user_type: str, db: Session):
    if user_type == "passenger":
        opinions, found = crud.get_opinions_passenger(id, db)
        if not opinions and not found:
            raise exceptions.PassengerNotFoundError
        return opinions
    else:
        opinions, found = crud.get_opinions_driver(id, db)
        if not opinions and not found:
            raise exceptions.DriverNotFoundError
        return opinions


def get_especific_user_by_id(id: int, user_type: str, db: Session):
    if user_type == "passenger":
        user = crud.get_passenger_by_id(id, db)
        if not user:
            raise exceptions.PassengerNotFoundError
        return user
    else:
        user = crud.get_driver_by_id(id, db)
        if not user:
            raise exceptions.DriverNotFoundError
        return user


def read_users(user_type: str, db: Session):
    if user_type == "passenger":
        return crud.get_passengers(db)
    else:
        return crud.get_drivers(db)


def get_users(db):
    return crud.get_users(db)


def create_user(token_id: Union[str, None], user: schema.UserBase, db: Session):
    if user.user_type == "passenger":
        user_create = crud.create_passenger(token_id, user, db)
    else:
        user_create = crud.create_driver(token_id, user, db)
    crud.logger.info(
        "Register user",
        extra={
            "type": "INFO",
            "endpoint": "/users",
            "method": "POST",
            "operation": "Register",
            "status": 200,
        },
    )
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


def score_user(user_id, user: schema.UserScore, db: Session):

    if user.user_type == "passenger":
        db_driver = crud.get_driver_by_id(user_id, db)
        if not db_driver:
            raise exceptions.DriverNotFoundError
        return crud.update_score_driver(db_driver, user, db)
    else:
        db_passenger = crud.get_passenger_by_id(user_id, db)
        if not db_passenger:
            raise exceptions.PassengerNotFoundError
        return crud.update_score_passenger(db_passenger, user, db)


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


def verified_user(email: str, db: Session):
    db_user = crud.get_user_by_email(email, db)
    return db_user


def login_verify_user_type(id, user_type, login_type, db):
    if user_type == "passenger":
        user = crud.get_passenger_by_id(id, db)
        if not user:
            crud.logger.warning(
                "Login with " + login_type + ", passenger does not exists ",
                extra={
                    "type": "WARN",
                    "endpoint": "/users/loginEmail",
                    "method": "POST",
                    "operation": "login",
                    "status": 409,
                },
            )
            raise exceptions.PassengerNotFoundError
        return user
    else:
        user = crud.get_driver_by_id(id, db)
        if not user:
            crud.logger.warning(
                "Login with " + login_type + ", driver does not exists ",
                extra={
                    "type": "WARN",
                    "endpoint": "/users/loginEmail",
                    "method": "POST",
                    "operation": "login",
                    "status": 409,
                },
            )
            raise exceptions.DriverNotFoundError
        return user


def login(email: str, token_id: str, user_type: str, db: Session):

    db_user = verified_user(email, db)
    if db_user is None:
        crud.logger.warning(
            "Login with email, cannot find user ",
            extra={
                "type": "WARN",
                "endpoint": "/users/loginEmail",
                "method": "POST",
                "operation": "login",
                "status": 409,
            },
        )
        raise exceptions.UserWrongLoginInformation
    if not token_id == db_user.tokenId:
        crud.logger.warning(
            "Login with email, invalid uid",
            extra={
                "type": "WARN",
                "endpoint": "/users/loginGoogle",
                "method": "POST",
                "operation": "login",
                "status": 409,
            },
        )
        raise exceptions.UserWrongLoginInformation
    login_verify_user_type(db_user.id, user_type, "email", db)
    crud.logger.info(
        "Login with email",
        extra={
            "type": "INFO",
            "endpoint": "/users/loginEmail",
            "method": "POST",
            "operation": "login",
            "status": 200,
        },
    )
    token = token_handler.create_access_token(db_user.id, "user")
    return token


def login_google(
    uid: str, email: str, name: str, picture: str, user_type: str, db: Session
):
    isnewUser = False
    user_id = -1
    if user_type == "passenger":
        relationship_passenger = crud.get_google_relationship_passenger(uid, db)
        if not relationship_passenger:
            user = crud.create_user_google_passenger(uid, email, name, picture, db)
            if user is None:
                raise exceptions.PassengerAlreadyExists
            user_id = user.id
            isnewUser = True
        else:
            user_id = relationship_passenger.userId
            crud.logger.info(
                "Login with Google",
                extra={
                    "type": "INFO",
                    "endpoint": "/users/loginGoogle",
                    "method": "POST",
                    "operation": "login",
                    "status": 200,
                },
            )
    else:
        relationship_driver = crud.get_google_relationship_driver(uid, db)
        if not relationship_driver:
            user = crud.create_user_google_driver(uid, email, name, picture, db)
            if user is None:
                raise exceptions.DriverAlreadyExists
            user_id = user.id
            isnewUser = True

        else:
            user_id = relationship_driver.userId
            crud.logger.info(
                "Login with Google",
                extra={
                    "type": "INFO",
                    "endpoint": "/users/loginGoogle",
                    "method": "POST",
                    "operation": "login",
                    "status": 200,
                },
            )
    return user_id, isnewUser


def verify_unique_user(id: int, type: str, db: Session):
    if type == "passenger":
        user = crud.get_driver_by_id(id, db)
        if user is not None:
            return False
        return True
    else:
        user = crud.get_passenger_by_id(id, db)
        if user is not None:
            return False
        return True


def delete_user(user_id, user_type, db: Session):
    if user_type == "passenger":
        google_user = crud.get_passenger_google_by_id(user_id, db)
        if google_user is not None:
            crud.delete_google_user_passenger(google_user, db)
        user = crud.delete_passenger(user_id, db)
        return user
    else:
        google_user = crud.get_driver_google_by_id(user_id, db)
        if google_user is not None:
            crud.delete_google_user_driver(google_user, db)
        user = crud.delete_driver(user_id, db)
        return user


def get_user_by_id(user_id: int, db: Session):
    user = crud.get_user_by_id(user_id, db)
    if not user:
        raise exceptions.UserNotFoundError
    return user


def block_user(user, block: bool, db: Session):
    return crud.toggle_block_user(user, block, db)
