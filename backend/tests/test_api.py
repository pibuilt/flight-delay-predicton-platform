from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_endpoint():

    sample_input = {
        "AIRLINE": "AA",
        "ORIGIN_AIRPORT": "JFK",
        "DESTINATION_AIRPORT": "LAX",
        "DEPARTURE_TIME": 900,
        "DISTANCE": 2475,
        "DAY_OF_WEEK": 3
    }

    response = client.post("/predict", json=sample_input)

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "prediction" in data["data"]
    assert "delay_probability" in data["data"]


def test_predict_invalid_input():

    bad_input = {
        "AIRLINE": "AA"
    }

    response = client.post("/predict", json=bad_input)

    assert response.status_code == 422