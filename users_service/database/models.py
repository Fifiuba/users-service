from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("user_name", String(50), nullable=False)
    # email = Column(String, unique=True, index=True)
    hashed_password = Column("password", String(50), nullable=False)
    phone_number = Column("phone_number", String(50), nullable=True)
    age = Column("age", Integer, nullable=True)
