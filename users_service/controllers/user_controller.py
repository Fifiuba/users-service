from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import sessionmaker
from typing import List
from users_service.database import crud, schema, exceptions


user_router = APIRouter()
session = None
Session = None


def set_engine(engine_rcvd):
    global engine
    global Session
    global session
    engine = engine_rcvd
    Session = sessionmaker(bind=engine)
    session = Session()


#@user_router.post(
#    "/createUser",
    #response_model=schema.UserResponse,
#    status_code=status.HTTP_201_CREATED,
#)
#async def registration(user: schema.UserBase):
#    try:
#        user_created = crud.create_user(user, session)
#        return user_created
#    except exceptions.UserInfoException as error:
#        raise HTTPException(**error.__dict__)


@user_router.get(
    "/getUsers",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users():
    users = crud.get_users(session)
    return users


@user_router.post(
    "/passenger/create",
    response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_passenger(user: schema.UserBase):
    try:
        user_create = crud.create_passenger(user, session)
        return user_create
    except exceptions.PassengerAlreadyExists as error:
        raise HTTPException(**error.__dict__)
        
        
@user_router.post(
    "/driver/create",
    response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_driver(user: schema.UserBase):
    try:
        user_create = crud.create_driver(user, session)
        return user_create
    except exceptions.DriverAlreadyExists as error:
        raise HTTPException(**error.__dict__)
   


@user_router.patch("/passenger/add_addres", status_code=status.HTTP_200_OK)
async def add_address(passenger: schema.PassengerBase):
    try:
        passenger = crud.add_passenger_address(passenger, session)
        return passenger
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/driver/add_car_info", status_code=status.HTTP_200_OK)
async def add_car_info(driver: schema.DriverBase):
    try:
        driver = crud.add_driver_car_info(driver, session)
        return driver
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)
