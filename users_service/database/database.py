# flake8: noqa

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from users_service.database.models import Base


def init_database():
    engine = create_engine(
        "postgresql://postgres:postgres@postgres:5432/users", echo=True
    )
    global SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    ##Base.metadata.drop_all(engine)
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
