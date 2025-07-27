import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///:memory:"  # In-memory DB for tests
    )
    with app.app_context():
        db.create_all()
    yield app.test_client()
    with app.app_context():
        db.drop_all()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Flask App!" in response.data


def test_create_item(client):
    response = client.post("/items", json={"name": "Test Item"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Test Item"


def test_get_items(client):
    # First, create an item
    client.post("/items", json={"name": "Test 1"})
    # Then, fetch all items
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.get_json()) >= 1
