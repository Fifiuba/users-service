from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

if "RUN_ENV" in os.environ.keys() and os.environ["RUN_ENV"] == "test":

    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

else:

#     engine = create_engine(
#         "postgresql+psycopg2://postgres:postgres@postgres:5432/users", echo=True
#     )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
    engine = create_engine("postgresql+psycopg2://postgres:postgres@postgres:5432/users" , echo=True )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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