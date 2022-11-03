from typing import Union
from sqlalchemy.orm import Session
from . import crud, schema, exceptions
from users_service.utils import token_handler


def get_user_by_email(email: str, db: Session):
    user = crud.get_user_by_email(email, db)
    if not user:
        raise exceptions.UserNotFoundError
    return user


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
        return crud.update_score_driver(db_driver, user.score, db)
    else:
        db_passenger = crud.get_passenger_by_id(user_id, db)
        if not db_passenger:
            raise exceptions.PassengerNotFoundError
        return crud.update_score_passenger(db_passenger, user.score, db)


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


def login(email, token_id, db: Session):

    db_user = verified_user(email, db)
    if db_user is None:
        crud.logger.warning("Login with email", extra={'type': 'WARN', 
                                                        'endpoint': '/users/loginEmail',
                                                         'method': 'POST', 
                                                         'operation': 'login',
                                                         'status': 409})
        raise exceptions.UserWrongLoginInformation
    if not token_id == db_user.tokenId:
        crud.logger.warning("Login with email", extra={'type': 'WARN', 
                                                        'endpoint': '/users/loginGoogle',
                                                         'method': 'POST', 
                                                         'operation': 'login',
                                                         'status': 409})
        raise exceptions.UserWrongLoginInformation
    crud.logger.info("Login with email", extra={'type': 'INFO', 
                                                'endpoint': '/users/loginEmail',
                                                'method': 'POST', 
                                                'operation': 'login',
                                                'status': 200})
    token = token_handler.create_access_token(db_user.id, "user")
    return token


def login_google(
    uid: str, email: str, name: str, picture: str, user_type: str, db: Session
):
    relationship = crud.get_google_relationship(uid, db)
    if not relationship:
        print("email: ", email)
        user = crud.get_user_by_email(email, db)
        if user:
            crud.logger.warning("Login with Goggle", extra={'type': 'WARN', 
                                                        'endpoint': '/users/loginGoogle',
                                                         'method': 'POST', 
                                                         'operation': 'login',
                                                         'status': 401})
            raise exceptions.UserAlreadyExists
        else:
            user_aux = schema.UserBase(
                user_type=user_type,
                name=name,
                password="",
                phone_number=None,
                email=email,
                age=None,
                picture=picture,
            )
            db_user = create_user(uid, user_aux, db)
            crud.logger.info("Login with Goggle", extra={'type': 'INFO', 
                                                        'endpoint': '/users/loginGoogle',
                                                         'method': 'POST', 
                                                         'operation': 'login',
                                                         'status': 200})
            crud.create_google_relationship(uid, db_user.id, db)
            user_id = db_user.id
    else:
        
        user_id = relationship.userId
        crud.logger.info("Login with Goggle", extra={'type': 'INFO', 
                                                        'endpoint': '/users/loginGoogle',
                                                         'method': 'POST', 
                                                         'operation': 'login',
                                                         'status': 200})

    token = token_handler.create_access_token(user_id, "user")
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
