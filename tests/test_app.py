import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app



def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"
    assert data["version"] == "1.0.0"


def test_prediction_success():
    client = app.test_client()

    response = client.post("/predict", json={"value": 10})

    assert response.status_code == 200

    data = response.get_json()
    assert data["input"] == 10
    assert data["prediction"] == 20


def test_prediction_missing_input():
    client = app.test_client()

    response = client.post("/predict", json={})

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data


def test_prediction_invalid_input():
    client = app.test_client()

    response = client.post("/predict", json={"value": "hello"})

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data