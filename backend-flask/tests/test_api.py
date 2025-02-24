from typing import Any

from flask.testing import FlaskClient


def test_dashboard_endpoint(client: FlaskClient, sample_data: Any) -> None:
    """Test dashboard endpoint returns correct statistics."""
    response = client.get("/api/dashboard/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True

    # Check structure matches specs
    assert "lastSession" in data["data"]
    assert "progress" in data["data"]
    assert "stats" in data["data"]

    # Check values
    assert data["data"]["stats"]["totalWords"] == 1
    assert data["data"]["progress"]["totalWordsLearned"] == 0
    assert data["data"]["stats"]["totalGroups"] == 1


"""
API Integration Tests

Tests the API endpoints to ensure they:
- Return correct status codes
- Return data in expected format
- Handle sample data correctly
"""
