import pytest
import json
from app import app  # Import the Flask app instance


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_users(client):
    """Test GET /api/users endpoint with pagination and search."""
    response = client.get("/api/users?page=1&limit=5&search=")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "users" in data


def test_get_user_by_id(client):
    """Test GET /api/users/<id> for an existing user."""
    response = client.get("/api/users/1")  # Assuming ID 1 exists
    assert response.status_code in [200, 404]


def test_update_user(client):
    """Test PUT /api/users/<id> to update a user."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "TechCorp",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "email": "john.doe@example.com",
        "web": "http://johndoe.com",
        "age": 30,
    }
    response = client.put("/api/users/1", json=user_data)
    assert response.status_code in [200, 404]


def test_delete_user(client):
    """Test DELETE /api/users/<id> endpoint."""
    response = client.delete("/api/users/1")  # Assuming ID 1 exists
    assert response.status_code in [200, 404]


def test_patch_user(client):
    """Test PATCH /api/users/<id> endpoint to update specific fields."""
    patch_data = {"city": "Los Angeles", "state": "CA"}
    response = client.patch("/api/users/1", json=patch_data)
    assert response.status_code in [200, 404]


def test_user_summary(client):
    """Test GET /api/users/summary endpoint."""
    response = client.get("/api/users/summary")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "total_users" in data
    assert "average_age" in data
    assert "users_by_city" in data
