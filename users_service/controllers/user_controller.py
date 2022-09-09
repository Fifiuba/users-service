from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker
from typing import List
from users_service.database import crud, schema

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


@user_router.post("/users/registration", tags=["users"])
async def registration(user: schema.UserBase):
    pass


@user_router.get("/users/", tags=["users"], response_model=List[schema.UserResponse])
def read_users(db: Session = Depends(crud.get_db)):
    users = crud.get_users(db)
    return users
