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


def registerClient(type):
    if type == "driver":
        response = client.post(
            "/users",
            json={
                "user_type": "driver",
                "name": "Sol",
                "password": "87654321",
                "phone_number": "12345678",
                "age": 22,
            },
        )
    else:
        response = client.post(
            "/users",
            json={
                "user_type": "passenger",
                "name": "Sol",
                "password": "87654321",
                "phone_number": "12345678",
                "age": 22,
            },
        )
    return response


def registerClient2(endpoint):
    response = client.post(
        endpoint,
        json={
            "name": "Agustina",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )
    return response


def addAdressClient(endpoint):
    response = client.patch(
        endpoint,
        json={"default_address": "Av avellaneda 123"},
    )
    return response


def addCarInfoClient(endpoint):
    response = client.patch(
        endpoint, json={"license_plate": "ABC123", "car_model": "Ford K"}
    )
    return response


def test_has_table():
    assert sa.inspect(engine).has_table("users")
    assert sa.inspect(engine).has_table("passengers")
    assert sa.inspect(engine).has_table("drivers")


def test_whenCreatingAPassengerWithNotRegisteredName_createsTheUserCorrectly():
    response = registerClient("passenger")

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Sol"
    # check de la hashed password?
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert "id" in data

    # faltaria chequear que el id devuelve al user correcto


def test_whenCreatingAPassengerWithRegisteredName_doesNotcreateThePassenger():
    registerClient("passenger")
    response = registerClient("passenger")

    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The passenger already exists"


def test_whenCreatingADriverWithNotRegisteredName_createsThePassengerCorrectly():
    response = registerClient("driver")

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Sol"
    # check de la hashed password?
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert "id" in data

    # faltaria chequear que el id devuelve al user correcto


def test_whenCreatingADriverWithRegisteredName_doesNotcreateTheDriver():
    registerClient("driver")
    response = registerClient("driver")
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The driver already exists"


def test_givenAPassangerThatExists_whenHeAddsanAddress_then_ItDoesAddTheAddres():
    response = registerClient2("users/passengers")
    data = response.json()
    response = addAdressClient("users/passengers/" + str(data["id"]))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert data["default_address"] == "Av avellaneda 123"


def test_givenAPassengerThatNotExists_whenHeAddsAnAddress_thenItDoesNotAddTheAddres():
    response = addAdressClient("users/passengers/100")
    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    assert data["detail"] == "The passenger does not exists"


def test_givenADriverThatExists_WhenHeAddsCarInfo_thenItDoesaddCarInfoCorrectly():
    response = registerClient2("users/drivers")
    data = response.json()
    response = addCarInfoClient("users/drivers/" + str(data["id"]))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert data["license_plate"] == "ABC123"
    assert data["car_model"] == "Ford K"


def test_givenADriverThtNotExists_WhenHeAddsCarInfo_ThenItDoesNotAddTheCarInfo():
    response = addCarInfoClient("users/drivers/100")
    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    assert data["detail"] == "The driver does not exists"
