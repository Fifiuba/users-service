from fastapi.testclient import TestClient
from fastapi import status
from users_service.app import app
from users_service.database.database import engine
import sqlalchemy as sa
from users_service.utils import token_handler


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
            "fields": [{}, {"default_address": "Av avellaneda 123"}],
        },
    )
    return response


def addCarInfoClient(endpoint):
    response = client.patch(
        endpoint,
        json={
            "user_type": "driver",
            "fields": [{}, {"license_plate": "ABC123", "car_model": "Ford K"}],
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

def test_when_app_has_2_passengers_then_get_passengers_return_2_users():
    registerPassenger()
    registerPassenger2()
    response = client.get("/users/passenger")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print(data)
    assert len(data) == 2
    client.delete("/users/" + str(data[0]["id"]), json={"user_type": "passenger"})
    client.delete("/users/" + str(data[1]["id"]), json={"user_type": "passenger"})

def test_when_app_has_2_user_then_get_users_return_2_users():

    registerPassenger()
    registerPassenger2()
    token = token_handler.create_access_token(2, True)
    response = client.get("/users/", headers={"Authorization": f"Baerer {token}"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2

    client.delete("/users/" + str(data[0]["id"]), json={"user_type": "passenger"})
    client.delete("/users/" + str(data[1]["id"]), json={"user_type": "passenger"})

def test_when_getting_a_passenger_info_that_existis_then_it_returns_it():
    response = registerPassenger()
    data = response.json()
    endpoint = "/users/info/" + str(data['id']) + "/passenger"
    response = client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK
    data1 = response.json()
    print("test ", data1)
    client.delete("/users/" + str(data["id"]), json={"user_type": "passenger"})

def test_when_creating_a_passenger_with_not_registered_email_creates_the_user():
    response = registerPassenger()

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()

    assert data["name"] == "Sol"
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert data["email"] == "sol@gmail.com"
    assert "id" in data
    client.delete("/users/" + str(data["id"]), json={"user_type": "passenger"})


def test_when_creating_passenger_with_registered_email_does_not_create_the_passenger():
    registerPassenger()
    response = registerPassenger()

    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The passenger already exists"

    client.delete("/users/1", json={"user_type": "passenger"})


def test_when_creating_a_driver_withnot_registered_email_creates_the_driver():
    response = registerDriver()

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()

    assert data["name"] == "Sol"
    assert data["email"] == "sol@gmail.com"
    assert data["phone_number"] == "12345678"
    assert data["age"] == 22
    assert "id" in data

    client.delete("/users/" + str(data["id"]), json={"user_type": "driver"})


def test_when_creating_driver_with_registered_email_doesnot_create_the_driver():
    registerDriver()
    response = registerDriver()
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    data = response.json()
    assert data["detail"] == "The driver already exists"
    client.delete("/users/1", json={"user_type": "driver"})


def test_when_a_passanger_exists_and_add_the_address_then_the_addres_is_add_it():
    response = registerPassenger2()
    data = response.json()
    id = data["id"]
    response = addAdressClient("/users/" + str(id))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert data[1]["default_address"] == "Av avellaneda 123"

    client.delete("/users/" + str(id), json={"user_type": "passenger"})


def test_when_Passenger_not_exist_and_adds_address_then_the_addres_isnot_addit():
    response = addAdressClient("/users/100")
    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    assert data["detail"] == "The passenger does not exists"


def test_when_driver_exists_and_adds_carInfo_the_carInfo_is_addit():
    response = registerDriver2()
    data = response.json()
    id = data["id"]
    response = addCarInfoClient("users/" + str(id))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert data[1]["license_plate"] == "ABC123"
    assert data[1]["car_model"] == "Ford K"

    client.delete("/users/" + str(id), json={"user_type": "driver"})


def test_when_driver_not_exists_and_adds_carInfo_the_carInfo_isnot_addit():
    response = addCarInfoClient("/users/100")
    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    assert data["detail"] == "The driver does not exists"


def test_when_getting_information_for_nonexisting_user_then_returns_user_not_exist():
    token = token_handler.create_access_token(1, True)
    response = client.get(
        "/users/info/1", headers={"Authorization": f"Baerer {token}"}
    )
    print(response.status_code)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

    data = response.json()

    assert data["detail"] == "The user does not exists"


def test_when_gettion_info_from_existing_user_then_returns_the_information():
    token = token_handler.create_access_token(1, True)
    response = registerPassenger2()
    data = response.json()

    response = client.get(
        "/users/info/" + str(data["id"]) , headers={"Authorization": f"Baerer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK, response.text

    data2 = response.json()

    assert data2["email"] == data["email"]
    assert data2["name"] == data["name"]
    assert data2["phone_number"] == data["phone_number"]
    assert data2["age"] == data["age"]

    client.delete("/users/" + str(data["id"]), json={"user_type": "passenger"})


def test_when_login_to_register_user_with_validad_data_then_it_should_return_token():
    response = registerPassenger2()
    response = client.post("users/login", json={"token": "hfjdshfuidhysvcsbvs83hfsdf"})
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    actual = token_handler.decode_token(data)
    expected = {
        "user_id": 1,
        "user": True,
    }

    assert actual["user_id"] == expected["user_id"]
    assert actual["user"] == expected["user"]
    client.delete("/users/" + str(1), json={"user_type": "passenger"})


def test_when_login_register_user_with_invalid_email_then_it_should_not_return_token():
    response = client.post("users/login", json={"token": "hfjdsvcsbvs83hfsdf"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    data = response.json()
    assert data["detail"] == "The username/password is incorrect"


def test_when_getting_profile_for_passenger_that_exists_it_should_do_it():
    response = registerPassenger2()
    data1 = response.json()
    token = token_handler.create_access_token(data1["id"], True)
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Baerer {token}"},
        json={"user_type": "passenger"},
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()

    assert data[0]["name"] == "Agus"
    assert data[0]["age"] == 22
    assert data[0]["phone_number"] == "12345678"
    assert data[0]["email"] == "agus@gmail.com"
    assert data[1]["default_address"] is None
    client.delete("/users/" + str(data1["id"]), json={"user_type": "passenger"})


def test_when_update_passenger_info_it_should_do_it():
    response = registerPassenger2()
    data1 = response.json()
    print(data1)
    token = token_handler.create_access_token(data1["id"], True)
    response = client.patch(
        "/users/me/",
        headers={"Authorization": f"Baerer {token}"},
        json={
            "user_type": "passenger",
            "fields": [{"age": 25}, {"default_address": "example"}],
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()

    assert data[0]["age"] == 25
    assert data[1]["default_address"] == "example"
    client.delete("/users/" + str(data1["id"]), json={"user_type": "passenger"})


def test_when_update_driver_info_it_should_do_it():
    response = registerDriver()
    data1 = response.json()
    token = token_handler.create_access_token(data1["id"], True)
    response = client.patch(
        "/users/me/",
        headers={"Authorization": f"Baerer {token}"},
        json={
            "user_type": "driver",
            "fields": [{"age": 14, "phone_number": "436278"}, {"model_car": "Audi"}],
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()

    assert data[0]["age"] == 14
    assert data[0]["phone_number"] == "436278"
    assert data[1]["model_car"] == "Audi"

    client.delete("/users/" + str(data1["id"]), json={"user_type": "driver"})


def test_when_update_driver_that_not_exist_it_should_not_do_it():
    token = token_handler.create_access_token(100, True)
    response = client.patch(
        "/users/me/",
        headers={"Authorization": f"Baerer {token}"},
        json={
            "user_type": "driver",
            "fields": [{"age": 14, "phone_number": "436278"}, {"model_car": "Audi"}],
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "The driver does not exists"


def test_when_update_passenger_that_not_exist_it_should_not_do_it():
    token = token_handler.create_access_token(100, True)
    response = client.patch(
        "/users/me/",
        headers={"Authorization": f"Baerer {token}"},
        json={
            "user_type": "passenger",
            "fields": [{"age": 25}, {"default_address": "example"}],
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "The passenger does not exists"

def test_when_login_with_google_with_user_not_register_then_it_returns_token():
    response = client.post("users/loginGoogle", json={"user_type": "passenger", "token": "hfjdshfuidhysvcsbvs83hfsdf"})
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    actual = token_handler.decode_token(data)
    expected = {
        "user_id": 1,
        "user": True,
    }

    assert actual["user_id"] == expected["user_id"]
    assert actual["user"] == expected["user"]
    client.delete("/users/" + str(1), json={"user_type": "passenger"})

# def test_when_login_with_google_when_user_register_normaly_does_not_return_token():
#     response = registerPassenger()
#     response = client.post("users/loginGoogle", json={"user_type": "passenger", "token": "hfjdshfuidhysvcsbvs83hfsdf"})
#     assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
#     data = response.json()
    
#     assert data['detail'] == "The user already exists"
    
#     client.delete("/users/" + str(1), json={"user_type": "passenger"})

def test_when_scoring_a_driver_that_exist_it_does_it():
    response = registerDriver()
    data = response.json()
    token = token_handler.create_access_token(100, True)
    endpoint = "/users/score/" + str(data['id'])
    print(endpoint)
    response = client.patch(endpoint, 
                headers={"Authorization": f"Baerer {token}"},
                json = {"user_type": "passenger", "score": 4},)
    assert response.status_code == status.HTTP_200_OK, response.text
    data1 = response.json()

    score_expected = (3 + 4)/2

    assert score_expected == data1['score']
    client.delete("/users/" + str(data['id']), json={"user_type": "driver"})

def test_when_scoring_a_driver_that_does_not_exist_it_does_not_do_it():
    token = token_handler.create_access_token(100, True)
    endpoint = "/users/score/101"
    print(endpoint)
    response = client.patch(endpoint, 
                headers={"Authorization": f"Baerer {token}"},
                json = {"user_type": "passenger", "score": 5},)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()
    assert data["detail"] == "The driver does not exists"