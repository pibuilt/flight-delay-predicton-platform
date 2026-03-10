from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

VALID_INPUT = {
    "AIRLINE": "AA",
    "ORIGIN_AIRPORT": "JFK",
    "DESTINATION_AIRPORT": "LAX",
    "DEPARTURE_TIME": 900,
    "DISTANCE": 2475,
    "DAY_OF_WEEK": 3,
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_endpoint():
    with TestClient(app) as c:
        response = c.post("/predict", json=VALID_INPUT)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "prediction" in data["data"]
    assert "delay_probability" in data["data"]


def test_predict_with_mocked_model():
    mock_model = MagicMock()
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [[0.7, 0.3]]

    with patch("backend.app.services.prediction_service.joblib.load", return_value=mock_model):
        with TestClient(app) as c:
            response = c.post("/predict", json=VALID_INPUT)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["prediction"] == 0
    assert data["data"]["delay_probability"] == 0.3


def test_predict_invalid_input():
    response = client.post("/predict", json={"AIRLINE": "AA"})
    assert response.status_code == 422


# --- Boundary tests ---

def test_boundary_day_of_week_zero():
    response = client.post("/predict", json={**VALID_INPUT, "DAY_OF_WEEK": 0})
    assert response.status_code == 422


def test_boundary_day_of_week_eight():
    response = client.post("/predict", json={**VALID_INPUT, "DAY_OF_WEEK": 8})
    assert response.status_code == 422


def test_boundary_departure_time_invalid():
    response = client.post("/predict", json={**VALID_INPUT, "DEPARTURE_TIME": 2400})
    assert response.status_code == 422


def test_boundary_distance_negative():
    response = client.post("/predict", json={**VALID_INPUT, "DISTANCE": -1})
    assert response.status_code == 422


def test_unknown_airline():
    response = client.post("/predict", json={**VALID_INPUT, "AIRLINE": "ZZ"})
    assert response.status_code == 422