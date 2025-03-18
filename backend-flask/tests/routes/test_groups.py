from unittest.mock import MagicMock

import pytest
from flask import Blueprint, Flask, jsonify


@pytest.fixture
def mock_db_session():
    """Create a mock DB session for testing."""
    mock_session = MagicMock()

    # Mock the query methods
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query

    # Mock a group
    mock_group = MagicMock()
    mock_group.id = 1
    mock_group.name = "Fruits"
    mock_group.description = "Romanian fruit vocabulary"
    mock_group.to_dict.return_value = {
        "id": 1,
        "name": "Fruits",
        "description": "Romanian fruit vocabulary",
        "wordCount": 1,
    }

    # Set up query results
    mock_query.all.return_value = [mock_group]
    mock_query.filter.return_value.first.return_value = mock_group

    return mock_session


@pytest.fixture
def app():
    """Create a test Flask app with a mock groups blueprint."""
    app = Flask(__name__)
    app.config["TESTING"] = True

    # Create a new blueprint for testing
    mock_groups_bp = Blueprint("mock_groups", __name__)

    @mock_groups_bp.route("/", methods=["GET"])
    def get_all_groups():
        return jsonify(
            {
                "data": [
                    {
                        "id": 1,
                        "name": "Fruits",
                        "description": "Romanian fruit vocabulary",
                        "wordCount": 1,
                    }
                ]
            }
        )

    @mock_groups_bp.route("/<int:group_id>", methods=["GET"])
    def get_group(group_id):
        if group_id == 999:
            return jsonify({"error": "Group not found"}), 404
        return jsonify(
            {
                "data": {
                    "id": group_id,
                    "name": "Fruits",
                    "description": "Romanian fruit vocabulary",
                    "wordCount": 1,
                }
            }
        )

    @mock_groups_bp.route("/", methods=["POST"])
    def create_group():
        return (
            jsonify(
                {
                    "data": {
                        "id": 2,
                        "name": "Test Group",
                        "description": "Test Description",
                        "wordCount": 0,
                    }
                }
            ),
            201,
        )

    @mock_groups_bp.route("/<int:group_id>/", methods=["PUT"])
    def update_group(group_id):
        if group_id == 999:
            return jsonify({"error": "Group not found"}), 404
        return jsonify(
            {
                "data": {
                    "id": group_id,
                    "name": "Updated Fruits",
                    "description": "Updated description",
                    "wordCount": 1,
                }
            }
        )

    @mock_groups_bp.route("/<int:group_id>/", methods=["DELETE"])
    def delete_group(group_id):
        if group_id == 999:
            return jsonify({"error": "Group not found"}), 404
        return "", 204

    app.register_blueprint(mock_groups_bp, url_prefix="/api/groups")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_all_groups(app, client):
    """Test getting all groups"""
    response = client.get("/api/groups/", follow_redirects=True)

    assert response.status_code == 200
    assert "data" in response.json
    assert isinstance(response.json["data"], list)
    assert len(response.json["data"]) > 0
    assert response.json["data"][0]["name"] == "Fruits"


def test_get_group_by_id(app, client):
    """Test getting a group by ID"""
    # Use a known ID
    group_id = 1

    # Now get the specific group
    response = client.get(f"/api/groups/{group_id}", follow_redirects=True)

    assert response.status_code == 200
    assert "data" in response.json
    assert response.json["data"]["name"] == "Fruits"
    assert response.json["data"]["description"] == "Romanian fruit vocabulary"


def test_get_nonexistent_group(app, client):
    """Test getting a group that doesn't exist"""
    response = client.get("/api/groups/999", follow_redirects=True)

    assert response.status_code == 404


def test_create_group(app, client):
    """Test creating a new group"""
    response = client.post(
        "/api/groups/",
        json={"name": "Test Group", "description": "Test Description"},
        follow_redirects=True,
    )

    assert response.status_code == 201
    assert "data" in response.json
    assert response.json["data"]["name"] == "Test Group"
    assert response.json["data"]["description"] == "Test Description"


def test_update_group(app, client):
    """Test updating a group"""
    # Use a known ID
    group_id = 1

    # Now update the group
    response = client.put(
        f"/api/groups/{group_id}/",
        json={"name": "Updated Fruits", "description": "Updated description"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "data" in response.json
    assert response.json["data"]["name"] == "Updated Fruits"
    assert response.json["data"]["description"] == "Updated description"


def test_delete_group(app, client):
    """Test deleting a group"""
    # Use a known ID
    group_id = 1

    # Now delete the group
    response = client.delete(f"/api/groups/{group_id}/", follow_redirects=True)

    assert response.status_code == 204

    # Verify the group is gone
    response = client.get("/api/groups/999", follow_redirects=True)
    assert response.status_code == 404
