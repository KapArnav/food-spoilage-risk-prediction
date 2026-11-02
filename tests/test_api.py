from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app, get_bundle


def client() -> TestClient:
    get_bundle.cache_clear()
    return TestClient(app)


def test_health() -> None:
    response = client().get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_info_uses_saved_metrics() -> None:
    response = client().get("/model-info")
    assert response.status_code == 200
    payload = response.json()
    assert payload["metrics"]["accuracy"] == 0.9926062846580407
    assert "future spoilage" in payload["limitations"][0].lower()


def test_predict_uses_existing_artifacts() -> None:
    response = client().post(
        "/predict",
        json={"fruit": "Orange", "temp": 22, "humid": 95, "light": 7.358649263, "co2": 361},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["predicted_class"] in {"Good", "Bad"}
    assert 0 <= payload["probability_bad"] <= 1
    assert 0 <= payload["probability_good"] <= 1


def test_predict_rejects_invalid_humidity() -> None:
    response = client().post(
        "/predict",
        json={"fruit": "Orange", "temp": 22, "humid": 120, "light": 7, "co2": 361},
    )
    assert response.status_code == 422
