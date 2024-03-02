from .utils import *
from fastapi import status
from app.database import get_db
from app.oauth2 import get_current_user

app.dependency_overrides[get_db]  = override_get_db

def test_login(test_user):
    request_data = {
        'username': 'john@email.com',
        'password': 'password123'
    }

    response = client.post('/login', data=request_data)#'data' for form-data
    assert response.status_code == status.HTTP_200_OK

    user = get_current_user(response.json()['token'])#no need to override get_current_user here

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.email == 'john@email.com').first()

    assert user.get('username') == model.email
    assert user.get('user_id') == model.id
    assert user.get('user_role') == model.role



def test_login_no_user(test_user):
    request_data = {
        'username': 'fakeuser@email.com',
        'password': 'password123'
    }

    response = client.post('/login', data=request_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Invalid credentials'}



def test_login_different_password(test_user):
    request_data = {
        'username': 'john@email.com',
        'password': 'fakepassword'
    }

    response = client.post('/login', data=request_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Invalid credentials'}