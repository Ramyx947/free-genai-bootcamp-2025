import pytest
import json

def test_health_check(client):
    response = client.get('/api/health/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_words(client, sample_data):
    response = client.get('/api/words/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
    assert 'data' in data
    assert len(data['data']) > 0

def test_get_groups(client):
    response = client.get('/api/groups/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
    assert 'data' in data

def test_create_group(client):
    group_data = {
        'name': 'Test Group',
        'description': 'Test Description'
    }
    response = client.post(
        '/api/groups/',
        data=json.dumps(group_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['name'] == group_data['name'] 