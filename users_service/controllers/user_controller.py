from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from users_service.database import crud, schema, exceptions, database


user_router = APIRouter()



@user_router.get(
    "/getUsers",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users(db: Session = Depends(database.get_db)):
    users = crud.get_users(db)
    return users


@user_router.post(
    "/passenger/create",
    response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_passenger(user: schema.UserBase, db: Session = Depends(database.get_db)):
    try:
        user_create = crud.create_passenger(user, db)
        return user_create
    except exceptions.PassengerAlreadyExists as error:
        raise HTTPException(**error.__dict__)


@user_router.post(
    "/driver/create",
    response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_driver(user: schema.UserBase, db: Session = Depends(database.get_db)):
    try:
        user_create = crud.create_driver(user, db)
        return user_create
    except exceptions.DriverAlreadyExists as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/passenger/add_address", status_code=status.HTTP_200_OK)
async def add_address(passenger: schema.PassengerBase, db: Session = Depends(database.get_db)):
    try:
        passenger = crud.add_passenger_address(passenger, db)
        return passenger
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/driver/add_car_info", status_code=status.HTTP_200_OK)
async def add_car_info(driver: schema.DriverBase, db: Session = Depends(database.get_db)):
    try:
        driver = crud.add_driver_car_info(driver, db)
        return driver
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: schema.UserLogInBase, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.get_user_log_in(user, db)
        return db_user
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)
