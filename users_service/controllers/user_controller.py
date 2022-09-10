from logging import exception
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


@user_router.post(
    "/createUser",
    #response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registration(user: schema.UserBase):
    try:
        user_created = crud.create_user(user, session)
        return user_created
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)



@user_router.get(
    "/getUsers",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users():
    users = crud.get_users(session)
    return users

@user_router.post("/createPassenger", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED)
async def registrate_passenger(user: schema.UserBase):
    try:
        user_create = crud.create_user(user, session)
        crud.create_passenger(user_create.id, session)
        return user_create
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)

@user_router.post("/create_driver",response_model=schema.UserResponse, status_code = status.HTTP_201_CREATED)
async def registrate_driver(user: schema.UserBase):
    try:
        user_create = crud.create_user(user, session)
        crud.create_driver(user_create.id, session)
        return user_create
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)

