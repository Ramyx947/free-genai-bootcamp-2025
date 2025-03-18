"""API route tests.

Tests for core API endpoints:
- Health check
- Word retrieval
- Group management
"""

import json

import pytest
from flask.testing import FlaskClient

from app import db
from app.models import Group, Word


@pytest.fixture(autouse=True)
def setup_database(app) -> None:
    """Set up test database with sample data before each test."""
    with app.app_context():
        # Create test data
        word = Word(
            romanian="test", english="test", part_of_speech="noun", parts=["test"]
        )
        group = Group(name="Test Group", description="Test description")

        db.session.add(word)
        db.session.add(group)
        db.session.commit()

        yield

        # Clean up
        Word.query.delete()
        Group.query.delete()
        db.session.commit()


def test_health_check(client: FlaskClient) -> None:
    """Test health check endpoint returns correct status and data."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_get_words(client: FlaskClient) -> None:
    """Test words endpoint returns properly formatted list of words."""
    response = client.get("/api/words")
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify response structure
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0


def test_get_groups(client: FlaskClient) -> None:
    """Test groups endpoint returns properly formatted list of groups."""
    response = client.get("/api/groups")
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify response structure
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0


def test_create_group(client: FlaskClient) -> None:
    """Test group creation with valid data returns success and created group."""
    response = client.post(
        "/api/groups", json={"name": "New Group", "description": "New description"}
    )
    assert response.status_code == 201
    data = json.loads(response.data)

    # Verify response structure and data
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["name"] == "New Group"
    assert data["data"]["description"] == "New description"
