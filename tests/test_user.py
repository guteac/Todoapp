from .utils import *
from fastapi import status
from app.oauth2 import get_current_user
from app.database import get_db

app.dependency_overrides[get_db]  = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_create_user(test_user):
    request_data = {
        'username': 'sampiper',
        'email': 'sam@email.com',
        'first_name': 'Sam',
        'last_name': 'Piper',
        'password': 'password123',
        'role': 'nonadmin',
        'phone_number': '(111)-111-1111',
        'is_active': True
    }

    response = client.post('/user', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 2).first()

    assert model.username == 'sampiper'



def test_change_password(test_user):
    request_data = {
        'current_password': 'password123',
        'new_password': 'password1234'
    }

    response = client.put('/user/password', json=request_data)
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()

    assert verify_credentials('password1234', model.password) == True



def test_change_password_unauthorized(test_user):
    request_data = {
        'current_password': 'fakepassword',
        'new_password': 'password1234'
    }

    response = client.put('/user/password', json=request_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED



def test_get_my_user(test_user):

    response = client.get('/user/my_user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'johndoe'