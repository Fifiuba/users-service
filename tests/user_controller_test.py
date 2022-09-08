from fastapi.testclient import TestClient

from users_service.app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [{"username": "Rick"}, {"username": "Morty"}]
