from flask.testing import FlaskClient


def test_health_check(client: FlaskClient) -> None:
    response = client.get("/api/health/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_get_words(client, sample_data):
    response = client.get("/api/words/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) > 0
    assert "romanian" in data["data"][0]


def test_get_groups(client):
    response = client.get("/api/groups/")
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data
    assert "data" in data


def test_create_group(client):
    group_data = {"name": "Test Group", "description": "Test Description"}
    response = client.post(
        "/api/groups/", json=group_data, content_type="application/json"
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == group_data["name"]
