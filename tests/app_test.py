from fastapi.testclient import TestClient
from fastapi import status
from users_service.app import app
from users_service.database.database import get_db
from sqlalchemy.orm import sessionmaker
from users_service.database.database import engine
from users_service.database.models import Base
import sqlalchemy as sa


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


def registerClient(endpoint):
    response = client.post(
        endpoint,
        json={
            "name": "Sol",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )
    return response


def test_has_table():
    assert sa.inspect(engine).has_table("users")
    assert sa.inspect(engine).has_table("passengers")
    assert sa.inspect(engine).has_table("drivers")


def test_whenCreatingAPassengerWithNotRegisteredName_createsTheUserCorrectly():
    response = registerClient("users/passengers")

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Sol"
    # check de la hashed password?
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert "id" in data

    # faltaria chequear que el id devuelve al user correcto


def test_whenCreatingAPassengerWithRegisteredName_doesNotcreateThePassenger():
    registerClient("users/passengers")
    response = registerClient("users/passengers")

    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The passenger already exists"


def test_whenCreatingADriverWithNotRegisteredName_createsThePassengerCorrectly():
    response = registerClient("users/drivers")

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Sol"
    # check de la hashed password?
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert "id" in data

    # faltaria chequear que el id devuelve al user correcto


def test_whenCreatingADriverWithRegisteredName_doesNotcreateTheDriver():
    registerClient("users/drivers")
    response = registerClient("users/drivers")
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The driver already exists"
