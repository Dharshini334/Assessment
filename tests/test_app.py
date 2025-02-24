import pytest
from app import app  # Import your Flask app


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config["TESTING"] = True  # Enable test mode
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Tests if the home route returns a 200 response."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the API" in response.data  # Correct expected output


# Functinal test
def test_api_data(client):
    """Tests the /api/data endpoint."""
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json == {"message": "Here is your data"}  # Expected output
