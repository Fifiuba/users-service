from fastapi import APIRouter, status
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
    response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registration(user: schema.UserBase):
    if crud.user_exists(user.name, session):
        return exceptions.UserAlreadyExists
    user_created = crud.create_user(user, session)
    return user_created


@user_router.get(
    "/getUsers",
    response_model=List[schema.UserResponse],
    status_code=status.HTTP_200_OK,
)
def read_users():
    users = crud.get_users(session)
    return users
