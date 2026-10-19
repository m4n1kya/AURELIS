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
    """Verify 90-day evaluation output structure for a valid request ID."""
    reqs_resp = client.get("/api/requests")
    assert reqs_resp.status_code == 200
    first_req_id = reqs_resp.json()[0]["request_id"]

    response = client.get(f"/api/analyze/{first_req_id}")
    assert response.status_code == 200
    payload = response.json()
    assert "decision" in payload
    assert "forecast" in payload
    assert "spending_changes" in payload
    assert "meta" in payload
    assert payload["meta"]["request_id"] == first_req_id


def test_analyze_nonexistent_request():
    """Verify 404 HTTP status for nonexistent request ID."""
    response = client.get("/api/analyze/nonexistent_request_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
