from .utils import *
from fastapi import status
from app.models import Todos
from app.oauth2 import get_current_user
from app.database import get_db


app.dependency_overrides[get_db]  = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all_todos_for_logged_user(test_todo):#executes test_todo before and after this function
    response = client.get('/todo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': 'To water the plants', 'description': 'I need to water the plants everyday', 'priority': 4, 'complete': False,  'owner_id': 1, 'id': 1}]



def test_get_one_todo(test_todo):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title': 'To water the plants', 'description': 'I need to water the plants everyday', 'priority': 4, 'complete': False,  'owner_id': 1, 'id': 1}



def test_get_one_todo_not_found(test_todo):
    response = client.get('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}



def test_create_todo(test_todo):
    request_data = {
        'title': 'To feed the hamster',
        'description': 'I need to feed the hamster',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todo', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()

    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')



def test_update_todo(test_todo):
    request_data = {
        'title': 'To water the trees',
        'description': 'I need to water the trees every week',
        'priority': 3,
        'complete': False
    }
        
    response = client.put('/todo/1', json=request_data)
    
    assert response.status_code == status.HTTP_202_ACCEPTED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    
    assert model.title == 'To water the trees'



def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'To water the trees',
        'description': 'I need to water the trees every week',
        'priority': 3,
        'complete': False
    }
        
    response = client.put('/todo/999', json=request_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}



def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}