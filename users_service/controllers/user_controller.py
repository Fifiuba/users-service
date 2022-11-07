from email import header
from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Union
from users_service.database import schema, exceptions, database, user_repository
from users_service.utils import authorization_handler, token_handler, firebase_handler


user_router = APIRouter()

def validated_admin(headers):
    authorization_handler.is_auth(headers)
    token = authorization_handler.get_token(headers)
    user = token_handler.decode_token(token)["user"]
    authorization_handler.is_admin(user)


@user_router.get(
    "",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users(
    rq: Request, user_type: Union[str, None] = None, db: Session = Depends(database.get_db)
):
    try:
        validated_admin(rq.headers)
        if user_type is None:
            users = user_repository.get_users(db)
        else:
            users = user_repository.read_users(user_type, db)
        return users
    except (exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    id: int, user_type: str, db: Session = Depends(database.get_db)
):
    try:
        user = user_repository.get_especific_user_by_id(id, user_type, db)
        return user
    except (exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.get(
    "/info/{id}", status_code=status.HTTP_200_OK, response_model=schema.UserInfoResponse
)
async def get_user(rq: Request, id: int, db: Session = Depends(database.get_db)):
    try:
        authorization_handler.is_auth(rq.headers)
        user = user_repository.get_user_by_id(id, db)
        return user
    except (exceptions.UnauthorizeUser, exceptions.UserNotFoundError) as error:
        raise HTTPException(**error.__dict__)


@user_router.post(
    "",
    response_model=schema.UserRegisteredResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_user(
    user: schema.UserBase,
    db: Session = Depends(database.get_db),
    firebase=Depends(firebase_handler.get_fb),
):
    try:
        token_id = firebase.create_user(user.email, user.password)
        return user_repository.create_user(token_id, user, db)
    except (exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def edit_user(
    user_id: int, user: schema.UserPatch, db: Session = Depends(database.get_db)
):
    try:
        return user_repository.edit_user_info(user_id, user, db)
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user: schema.UserLogInBase,
    db: Session = Depends(database.get_db),
    firebase=Depends(firebase_handler.get_fb),
):
    try:
        user = firebase.valid_user(user.token)
        return user_repository.login(user.get("email"), user.get("uid"), db)
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/loginGoogle", status_code=status.HTTP_200_OK)
async def login_google(
    googleUser: schema.GoogleLogin,
    db: Session = Depends(database.get_db),
    firebase=Depends(firebase_handler.get_fb),
):
    try:
        user = firebase.valid_user(googleUser.token)
        email = firebase.get_email(user.get("uid"))
        print("email: ", email)
        return user_repository.login_google(
            user.get("uid"),
            email,
            user.get("name"),
            user.get("picture"),
            googleUser.user_type,
            db,
        )
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/me/", status_code=status.HTTP_200_OK)
async def edit_profile(
    rq: Request, user: schema.UserPatch, db: Session = Depends(database.get_db)
):
    try:
        authorization_handler.is_auth(rq.headers)
        token = authorization_handler.get_token(rq.headers)
        user_id = token_handler.decode_token(token)["user_id"]
        return user_repository.edit_user_info(user_id, user, db)
    except (exceptions.UnauthorizeUser, exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.get("/me/", status_code=status.HTTP_200_OK)
async def get_profile(
    rq: Request, user_type: str, db: Session = Depends(database.get_db)
):
    try:
        authorization_handler.is_auth(rq.headers)
        token = authorization_handler.get_token(rq.headers)
        user_id = token_handler.decode_token(token)["user_id"]
        return user_repository.user_profile(user_id, user_type, db)
    except (exceptions.UnauthorizeUser, exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    rq: Request,
    user_id: int,
    user: schema.TypeOfUser,
    db: Session = Depends(database.get_db),
    firebase=Depends(firebase_handler.get_fb),
):
    try:
        validated_admin(rq.headers)
        db_user = user_repository.get_user_by_id(user_id, db)
        firebase.delete_user(db_user.tokenId)
        user_repository.delete_user(user_id, user.user_type, db)
    except (exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/score/{user_id}", status_code=status.HTTP_200_OK)
async def score_user(
    rq: Request,
    user_id: int,
    user: schema.UserScore,
    db: Session = Depends(database.get_db),
):
    try:
        authorization_handler.is_auth(rq.headers)
        return user_repository.score_user(user_id, user, db)
    except (exceptions.UnauthorizeUser, exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)
