# app/tests/test_app.py

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'OK'

def test_crosspost_no_api_key(client):
    response = client.post('/crosspost/', json={"content": "Test content"})
    assert response.status_code == 429  # Rate limit exceeded since no API key

def test_crosspost_invalid_content(client):
    headers = {"X-API-Key": "testkey"}
    response = client.post('/crosspost/', headers=headers, json={"content": ""})
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data

def test_crosspost_valid_content(client, mocker):
    headers = {"X-API-Key": "testkey"}
    mocker.patch('app.utils.optimize_content', return_value="Optimized content")
    mocker.patch('app.tasks.post_content_task.delay', return_value=type('obj', (object,), {'id': '123'})())
    response = client.post('/crosspost/', headers=headers, json={"content": "Valid content"})
    assert response.status_code == 202
    json_data = response.get_json()
    assert "message" in json_data
    assert "tasks" in json_data