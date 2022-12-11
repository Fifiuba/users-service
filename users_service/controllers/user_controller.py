from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Union
from users_service.database import schema, exceptions, database, user_repository
from users_service.utils import authorization_handler, token_handler, firebase_handler, events_handler, wallet_handler


user_router = APIRouter()


def validated_admin(headers):
    authorization_handler.is_auth(headers)
    token = authorization_handler.get_token(headers)
    payload = token_handler.decode_token(token)
    user = payload["rol"]
    authorization_handler.is_admin(user)



@user_router.get(
    "",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users(
    rq: Request,
    user_type: Union[str, None] = None,
    db: Session = Depends(database.get_db),
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

@user_router.get("/opinions/{id}",  status_code=status.HTTP_200_OK)
async def get_opinions_user(rq: Request, id:int, user_type: str, db: Session = Depends(database.get_db)):
    try:
        authorization_handler.is_auth(rq.headers)
        return user_repository.get_opinions_users(id, user_type, db)
        
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
    events=Depends(events_handler.get_event),
    wallet=Depends(wallet_handler.get_wallet),
):
    try:

        token_id = firebase.create_user(user.email, user.password)
        value = user_repository.create_user(token_id, user, db)
        wallet.create_wallet(value.id)
        events.create_event("Register user with email", "A user was register", "info", ["type:INFO",
            "endpoint:/users",
            "method:POST",
            "operation:Register",
            "status:200"])
        return value
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
    userlogin: schema.UserLogInBase,
    db: Session = Depends(database.get_db),
    firebase=Depends(firebase_handler.get_fb),
    events=Depends(events_handler.get_event),
):
    try:
        user = firebase.valid_user(userlogin.token)
        token = user_repository.login(
            user.get("email"), user.get("uid"), userlogin.user_type, db
        )
        events.create_event("Login with Email", "A user login in the system via Email", "info", ["type:INFO",
            "type:INFO",
            "endpoint:/users/loginEmail",
            "method:POST",
            "operation:login",
            "status:200"])
        return token
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/loginGoogle", status_code=status.HTTP_200_OK)
async def login_google(
    googleUser: schema.GoogleLogin,
    db: Session = Depends(database.get_db),
    firebase=Depends(firebase_handler.get_fb),
    events=Depends(events_handler.get_event),
    wallet = Depends(wallet_handler.get_wallet)
):
    try:
        user = firebase.valid_user(googleUser.token)
        email = firebase.get_email(user.get("uid"))
        id, isNewUser= user_repository.login_google(
            user.get("uid"),
            email,
            user.get("name"),
            user.get("picture"),
            googleUser.user_type,
            db,
        )   
        wallet.create_wallet(id)
        if isNewUser :
            events.create_event("Register user with google", "A user registers the systems with google", "info", ["type:INFO",
                    "endpoint:/users/loginGoogle",
                    "method:POST",
                    "operation:Register",
                    "status:200",])

        events.create_event("Login with google", "A user login in the system via google", "info", ["type:INFO",
                    "endpoint:/users/loginGoogle",
                    "method:POST",
                    "operation:login",
                    "status:200",])  
        token = token_handler.create_access_token(id, "user")      
        return token
    except exceptions.UserInfoException as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/me/", status_code=status.HTTP_200_OK)
async def edit_profile(
    rq: Request, user: schema.UserPatch, db: Session = Depends(database.get_db)
):
    try:
        authorization_handler.is_auth(rq.headers)
        token = authorization_handler.get_token(rq.headers)
        id = token_handler.decode_token(token)["id"]
        return user_repository.edit_user_info(id, user, db)
    except (exceptions.UnauthorizeUser, exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.get("/me/", status_code=status.HTTP_200_OK)
async def get_profile(
    rq: Request, user_type: str, db: Session = Depends(database.get_db)
):
    try:
        authorization_handler.is_auth(rq.headers)
        token = authorization_handler.get_token(rq.headers)
        id = token_handler.decode_token(token)["id"]
        return user_repository.user_profile(id, user_type, db)
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
        unique = user_repository.verify_unique_user(user_id, user.user_type, db)
        if unique :
            firebase.delete_user(db_user.tokenId)
        return user_repository.delete_user(user_id, user.user_type, db)
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
        user = user_repository.score_user(user_id, user, db)
        return user
    except (exceptions.UnauthorizeUser, exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.patch("/block/{user_id}", status_code=status.HTTP_200_OK)
async def block_user( rq: Request, user_id: int, userBlock: schema.BlockUser, db: Session = Depends(database.get_db), firebase=Depends(firebase_handler.get_fb), events=Depends(events_handler.get_event)):
    try: 
        validated_admin(rq.headers)
        db_user = user_repository.get_user_by_id(user_id, db)
        print(db_user.id)
        firebase.block_user(db_user.tokenId, userBlock.block)
        
        user = user_repository.block_user(db_user, userBlock.block, db)
        if userBlock.block :
            events.create_event("Block User", "A user was block by an admin", "info", ["type:INFO",
                                    "endpoint:/users/block",
                                    "method:PATCH",
                                    "operation:block",
                                    "status:200",])
        else :
             events.create_event("Unlock User", "A user was unblock by an admin", "info", ["type:INFO",
                                    "endpoint:/users/block",
                                    "method:PATCH",
                                    "operation:unblock",
                                    "status:200",])
        return user
    except (exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)


@user_router.post("/restorePassword/{user_id}", status_code=status.HTTP_200_OK)
async def restore_password(rq: Request, user_id: int,db: Session = Depends(database.get_db), events=Depends(events_handler.get_event)):
    try:
        authorization_handler.is_auth(rq.headers)
        user = user_repository.get_user_by_id(user_id, db)
        events.create_event("Restore password User", "A user restore its password", "info", ["type:INFO",
                                    "endpoint:/users/restorePassword",
                                    "method:POST",
                                    "operation:restorePassword",
                                    "status:200",])
        return user
    except (exceptions.UserInfoException) as error:
        raise HTTPException(**error.__dict__)
