from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("user_name", String(255), nullable=False)
    # email = Column(String, unique=True, index=True)
    password = Column("password", String(255), nullable=False)
    phone_number = Column("phone_number", String(255), nullable=True)
    age = Column("age", Integer, nullable=True)
