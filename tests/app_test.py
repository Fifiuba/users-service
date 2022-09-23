from fastapi.testclient import TestClient
from fastapi import status
from users_service.app import app
from users_service.database.database import get_db
from sqlalchemy.orm import sessionmaker
from users_service.database.database import engine
from users_service.database.models import Base
import sqlalchemy as sa
from users_service.utils import token_handler


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
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


def registerDriver():
    response = client.post(
        "/users",
        json={
            "user_type": "driver",
            "name": "Sol",
            "email": "sol@gmail.com",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )
    return response


def registerPassenger():

    response = client.post(
        "/users",
        json={
            "user_type": "passenger",
            "name": "Sol",
            "email": "sol@gmail.com",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )
    return response


def registerDriver2():
    response = client.post(
        "/users",
        json={
            "user_type": "driver",
            "name": "Agus",
            "email": "agus@gmail.com",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )
    return response


def registerPassenger2():
    response = client.post(
        "/users",
        json={
            "user_type": "passenger",
            "name": "Agus",
            "email": "agus@gmail.com",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )
    return response


def addAdressClient(endpoint):
    response = client.patch(
        endpoint,
        json={
            "user_type": "passenger",
            "fields": [{"default_address": "Av avellaneda 123"}],
        },
    )
    return response


def addCarInfoClient(endpoint):
    response = client.patch(
        endpoint,
        json={
            "user_type": "driver",
            "fields": [{"license_plate": "ABC123", "car_model": "Ford K"}],
        },
    )
    return response


def test_has_table():
    assert sa.inspect(engine).has_table("users")
    assert sa.inspect(engine).has_table("passengers")
    assert sa.inspect(engine).has_table("drivers")


def test_when_app_is_with_no_users_then_get_users_return_an_empty_list():
    token = token_handler.create_access_token(1, True)
    response = client.get("/users/", headers={"Authorization": f"Baerer {token}"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == []

def test_when_app_has_2_user_then_get_users_return_2_users():
    client.post("/users", json={ "user_type": "passenger", 
                    "name": "Agus3","email": "agus3@gmail.com",
                    "password": "87654321", "phone_number": "12345678","age": 22,
                    },)
    client.post("/users", json={ "user_type": "passenger", 
                    "name": "Agus4","email": "agus4@gmail.com",
                    "password": "87654321", "phone_number": "12345678","age": 22,
                    },)
    token = token_handler.create_access_token(2, True)
    response = client.get("/users/", headers={"Authorization": f"Baerer {token}"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2
    print(data)
    
    

def test_when_creating_a_passenger_with_not_registered_email_creates_the_user():
    response = registerPassenger()

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Sol"
    # check de la hashed password?
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert data["email"] == "sol@gmail.com"
    assert "id" in data
    print(data)


#     # faltaria chequear que el id devuelve al user correcto


def test_when_creating_passenger_with_registered_email_doesnot_create_the_passenger():
    registerPassenger()
    response = registerPassenger()

    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The passenger already exists"


def test_when_creating_a_driver_withnot_registered_email_creates_the_driver(): 
    response = registerDriver()

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["name"] == "Sol"
     # check de la hashed password?
    assert data["email"] == "sol@gmail.com"
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert "id" in data

# faltaria chequear que el id devuelve al user correcto


def test_when_creating_driver_with_registered_email_doesnot_create_the_driver():
    registerDriver()
    response = registerDriver()
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The driver already exists"


def test_when_a_passanger_exists_and_add_the_address_then_the_addres_is_add_it():
    response = registerPassenger2()
    data = response.json()
    assert data["name"] == "Agus"
    response = addAdressClient("/users/" + str(data["id"]))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert data["default_address"] == "Av avellaneda 123"


def test_when_Passenger_not_exist_and_adds_address_then_the_addres_isnot_addit():
    response = addAdressClient("/users/100")
    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    assert data["detail"] == "The passenger does not exists"


def test_when_driver_exists_and_adds_carInfo_the_carInfo_is_addit():
    response = registerDriver2()
    data = response.json()

    response = addCarInfoClient("users/" + str(data["id"]))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert data["license_plate"] == "ABC123"
    assert data["car_model"] == "Ford K"


def test_when_driver_not_exists_and_adds_carInfo_the_carInfo_isnot_addit():
    response = addCarInfoClient("/users/100")
    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    assert data["detail"] == "The driver does not exists"


def test_when_getting_information_for_nonexisting_user_then_returns_user_not_exist():
    token = token_handler.create_access_token(1, True)
    response = client.get(
        "/users/EXAMPLE@gamil.com", headers={"Authorization": f"Baerer {token}"}
    )
    print(response.status_code)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

    data = response.json()
    print(data)
    assert data["detail"] == "The user does not exists"


def test_when_gettion_info_from_existing_user_then_returns_the_information():
    token = token_handler.create_access_token(1, True)
    response = client.post(
        "/users",
        json={
            "user_type": "passenger",
            "name": "Agus2",
            "email": "agus2@gmail.com",
            "password": "87654321",
            "phone_number": "12345678",
            "age": 22,
        },
    )
    data = response.json()

    response = client.get(
        "/users/" + data["email"], headers={"Authorization": f"Baerer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK, response.text

    data2 = response.json()

    assert data2["email"] == data["email"]
    assert data2["name"] == data["name"]
    assert data2["phone_number"] == data["phone_number"]
    assert data2["age"] == data["age"]

def test_when_login_to_register_user_with_validad_data_then_it_should_return_token():
    response = client.post(
        "users/login", json={"email": "agus3@gmail.com", "password": "87654321"}
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    actual = token_handler.decode_token(data)
    expected = {
        "user_id": 1,
        "user": True,
    }

    assert actual["user_id"] == expected["user_id"]
    assert actual["user"] == expected["user"]

def test_when_login_to_register_user_with_invalid_email_then_it_should_not_return_token():
    response = client.post(
        "users/login", json={"email": "AGUSTINA12345@gmail.com", "password": "87654321"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    data = response.json()
    assert data['detail'] == "The username/password is incorrect"

def test_when_login_to_register_user_with_invalid_password_then_it_should_not_return_token():
    response = client.post(
        "users/login", json={"email": "agus3@gmail.com", "password": "12345678"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    data = response.json()
    assert data['detail'] == "The username/password is incorrect"

