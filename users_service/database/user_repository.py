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


def create_user(user: schema.UserBase, db: Session):
    if user.user_type == "passenger":
        user_create = crud.create_passenger(user, db)
    else:
        user_create = crud.create_driver(user, db)
    return user_create


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


def verified_user(email, password: str, db: Session):
    db_user = crud.get_user_by_email(email, db)
    password_ok = False
    if db_user:
        password_ok = password_handler.verify_password(password, db_user.password)
    return db_user, password_ok


def login(user: schema.UserLogInBase, db: Session):

    db_user, password_ok = verified_user(user.email, user.password, db)
    if db_user is None or not password_ok:
        raise exceptions.UserWrongLoginInformation
    token = token_handler.create_access_token(db_user.id, True)
    return token


def login_google(googleUser: schema.GoogleLogin, db: Session):
    user_id = crud.login_google(googleUser, db)
    token = token_handler.create_access_token(user_id, True)
    return token
