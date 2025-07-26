import pytest
from app import app, items


@pytest.fixture
def client():
    app.config["TESTING"] = True
    items.clear()  # Ensure isolation between tests
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, Flask!" in response.data


def test_create_item(client):
    response = client.post("/items", json={"name": "Test Item"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Test Item"
