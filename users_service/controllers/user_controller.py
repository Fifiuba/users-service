from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from users_service.database import schema, exceptions, database, user_repository
from users_service.utils import authorization_handler


user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users(rq: Request, db: Session = Depends(database.get_db)):
    try:
        authorization_handler.is_auth(rq.headers)
    except (exceptions.UnauthorizeUser) as error:
        raise HTTPException(**error.__dict__)
    else:
        users = user_repository.get_users(db)
        return users


@user_router.get("/{email}", status_code=status.HTTP_200_OK)
async def get_user(rq: Request, email: str, db: Session = Depends(database.get_db)):
    try:
        authorization_handler.is_auth(rq.headers)
        user = user_repository.get_user_by_email(email, db)
        return user
    except (exceptions.UnauthorizeUser, exceptions.UserNotFoundError) as error:
        raise HTTPException(**error.__dict__)


@user_router.post(
    "",
    response_model=schema.UserRegisteredResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_user(
    user: schema.UserBase, db: Session = Depends(database.get_db)
):
    try:
        return user_repository.create_user(user, db)
    except (exceptions.PassengerAlreadyExists, exceptions.DriverAlreadyExists) as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def add_user_info(
    user_id: int, user: schema.UserPatch, db: Session = Depends(database.get_db)
):

    try:
        return user_repository.add_user_info(user_id, user, db)
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user: schema.UserLogInBase, db: Session = Depends(database.get_db)
):
    try:
        return user_repository.login(user, db)
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/loginGoogle", status_code=status.HTTP_200_OK)
async def login_google(
    googleUser: schema.GoogleLogin, db: Session = Depends(database.get_db)
):
    try:
        return user_repository.login_google(googleUser, db)
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)
