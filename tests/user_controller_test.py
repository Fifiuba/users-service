from fastapi.testclient import TestClient

from users_service.app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/users/")
    print("respuesta del get:" + response)
    assert response.status_code == 200
    assert response == []
