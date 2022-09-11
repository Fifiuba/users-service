from fastapi.testclient import TestClient
from fastapi import status
from users_service.app import app
from users_service.crud import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base

# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Create the new database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/createUser",
        json={
            "name": "Sol",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Sol"
    # check de la hashed password?
    assert data["password"] == "87654321"
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert "id" in data

    # faltaria chequear que el id devuelve al user correcto
