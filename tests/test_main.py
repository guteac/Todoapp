from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app)

def test_return_health_check():
    response = client.get('/healthy')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status' : 'Healthy'}

def test_return_welcom_page():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message' : 'Hello and Welcome!'}