from flask.testing import FlaskClient
import pytest
import json
from app import db
from app.models import Word, Group


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


def test_dashboard_endpoint(client: FlaskClient) -> None:
    """Test dashboard endpoint returns correct structure and data types."""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify response structure
    assert "data" in data
    assert "stats" in data["data"]
    assert "totalWords" in data["data"]["stats"]
    assert "totalGroups" in data["data"]["stats"]

    # Verify data types
    assert isinstance(data["data"]["stats"]["totalWords"], int)
    assert isinstance(data["data"]["stats"]["totalGroups"], int)


"""API Integration Tests.

Tests the API endpoints to ensure they:
- Return correct status codes
- Return data in expected format
- Handle sample data correctly
"""
