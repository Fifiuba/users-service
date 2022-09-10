from . import models, schema, exceptions
from sqlalchemy.orm import Session
from .database import SessionLocal

# TODO: Modular el hasher
from passlib.context import CryptContext

# from fastapi import Depends


# Dependency
def get_db():
    db = SessionLocal()()
    try:
        yield db
    finally:
        db.close()


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def get_users(db: Session):
    query_response = db.query(models.User).all()
    return query_response


def get_user_by_name(name: str, db: Session):
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_by_id(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()


def user_exists(username, db: Session):
    return get_user_by_name(username, db) is not None


def create_user(user: schema.UserBase, db: Session):
    if user_exists(user.name, db):
        return exceptions.UserAlreadyExists

    hashed_password = get_hashed_password(user.password)
    db_user = models.User(
        name=user.name,
        password=hashed_password,
        phone_number=user.phone_number,
        age=user.age,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
