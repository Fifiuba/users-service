from . import models, schema
from sqlalchemy.orm import Session
from .database import SessionLocal
#from .exceptions import UserAlreadyExist
from fastapi import Depends

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_users(db: Session = Depends(get_db)):
    query_response = db.query(models.User).all()
    return query_response


"""
def get_user_by_name(db: Session = Depends(get_db), name: str):
    return db.query(models.User).filter(models.User.user_name == name);
    
    
def get_user_by_id(db: Session = Depends(get_db), user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first():
    
def create_user(db: Session = Depends(get_db), user: schema.UserBase):
    hashed_password = ""
    query = get_user_by_name(db, user.name)
    if query.count != 0:
        raise UserAlreadyExists
    db_user = models.User(name=user.name, hashed_password=hashed_password, 
                        phone_number=user.phone_number,age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
"""
