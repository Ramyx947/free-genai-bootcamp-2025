import pytest
from app import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_dashboard_endpoint(client):
    response = client.get('/api/dashboard/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'data' in data
    assert 'total_words' in data['data']
    assert 'learned_words' in data['data']
