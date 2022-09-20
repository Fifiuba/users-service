from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from users_service.database import crud, schema, exceptions, database
from users_service.utils import token_handler


user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users(db: Session = Depends(database.get_db)):
    users = crud.get_users(db)
    return users


@user_router.post(
    "",
    response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_user(user: schema.UserBase, db: Session = Depends(database.get_db)):
    try:
        if(user.user_type == "passenger"):
            user_create = crud.create_passenger(user, db)
        else:
            user_create = crud.create_driver(user, db)
        return user_create
    except (exceptions.PassengerAlreadyExists, exceptions.DriverAlreadyExists) as error:
        raise HTTPException(**error.__dict__)

@user_router.patch("/passengers/{passenger_id}", status_code=status.HTTP_200_OK)
async def add_address(
    passenger_id: int, passenger: schema.PassengerBase, db: Session = Depends(database.get_db)
):

    try:
        passenger = crud.add_passenger_address(passenger_id, passenger, db)
        return passenger
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/drivers/{driver_id}", status_code=status.HTTP_200_OK)
async def add_car_info(
    driver_id:int, driver: schema.DriverBase, db: Session = Depends(database.get_db)
):
    try:
        driver = crud.add_driver_car_info(driver_id, driver, db)
        return driver
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user: schema.UserLogInBase, db: Session = Depends(database.get_db)
):
    try:
        user_id = crud.get_user_log_in(user, db)
        token = token_handler.create_access_token(user_id, True)
        return token
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/loginGoogle", status_code=status.HTTP_200_OK)
async def login_google(googleUser: schema.GoogleLogin, db: Session = Depends(database.get_db)):
    try:
        user_id = crud.login_google(googleUser, db)
        token = token_handler.create_access_token(user_id, True)
        return token
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


