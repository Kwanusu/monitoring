import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_item(client):
    response = client.post('/items', json={"name": "Test Item"})
    assert response.status_code == 201
    assert response.json["name"] == "Test Item"
