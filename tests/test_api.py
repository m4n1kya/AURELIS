"""
Automated Integration Tests for AURELIS REST API
================================================

Validates health status, request catalog retrieval, 90-day simulation analysis,
and 404 error handling for invalid request identifiers.
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_read_health():
    """Verify health endpoint contract and engine mode."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "engine": "deterministic"}
    assert "x-process-time" in response.headers


def test_list_requests():
    """Verify listing all requests returns populated metadata items."""
    response = client.get("/api/requests")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "request_id" in data[0]
    assert "user_id" in data[0]
    assert "amount" in data[0]


def test_analyze_valid_request():
    """Verify 90-day evaluation output structure and frontend contract for a valid request ID."""
    reqs_resp = client.get("/api/requests")
    assert reqs_resp.status_code == 200
    first_req_id = reqs_resp.json()[0]["request_id"]

    response = client.get(f"/api/analyze/{first_req_id}")
    assert response.status_code == 200
    payload = response.json()
    assert "decision" in payload
    assert "forecast" in payload
    assert "timeline" in payload
    assert "state" in payload
    assert "events" in payload["state"]
    assert len(payload["state"]["events"]) > 0
    first_ev = payload["state"]["events"][0]
    assert "event_date" in first_ev
    assert "category" in first_ev
    assert "amount" in first_ev
    assert "direction" in first_ev
    assert "spending_changes" in payload
    assert "meta" in payload
    assert payload["meta"]["request_id"] == first_req_id


def test_analyze_nonexistent_request():
    """Verify 404 HTTP status for nonexistent request ID."""
    response = client.get("/api/analyze/nonexistent_request_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_metrics_valid_request():
    """Verify financial health indicators retrieval for a valid request ID."""
    reqs_resp = client.get("/api/requests")
    assert reqs_resp.status_code == 200
    first_req_id = reqs_resp.json()[0]["request_id"]

    response = client.get(f"/api/metrics/{first_req_id}")
    assert response.status_code == 200
    payload = response.json()
    assert payload["request_id"] == first_req_id
    assert "metrics" in payload
    metrics = payload["metrics"]
    assert "liquidity_ratio" in metrics
    assert "emergency_fund_ratio_months" in metrics
    assert "margin_of_safety" in metrics
    assert "discretionary_spending_ratio" in metrics
    assert "cash_runway_months" in metrics
    assert "debt_to_income_ratio" in metrics


def test_metrics_nonexistent_request():
    """Verify 404 HTTP status for metrics on nonexistent request ID."""
    response = client.get("/api/metrics/nonexistent_request_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

