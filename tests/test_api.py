from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_structured_response():
    response = client.post("/predict", json={"text": "call mom"})
    assert response.status_code == 200

    body = response.json()
    assert "intent" in body
    assert "confidence" in body
    assert "entities" in body
    assert "route" in body
    assert 0.0 <= body["confidence"] <= 1.0


def test_stats_endpoint_returns_summary():
    response = client.get("/stats")
    assert response.status_code == 200

    body = response.json()
    assert "total" in body
    assert "avg_confidence" in body
