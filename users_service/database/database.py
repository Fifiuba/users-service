# flake8: noqa
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from users_service.database.models import Base
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def init_database():
    DB_URL = os.getenv("DATABASE_URL")
    engine = create_engine(
        DB_URL, echo=True
    )
    global SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(engine)


def get_local_session():
    return SessionLocal()


# Dependency
def get_db():
    db = SessionLocal()
    print(db)
    try:
        yield db
    finally:
        db.close()
