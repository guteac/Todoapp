from .utils import *
from fastapi import status
from app.models import Todos
from app.oauth2 import get_current_user
from app.database import get_db


app.dependency_overrides[get_db]  = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_get_all_todos(test_todo_admin):
    response = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': 'Go to the gym', 'description': 'I need to go to the gym three time a week!', 'priority': 4, 'complete': False,  'owner_id': 2, 'id': 1}]



def test_admin_delete_todo(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None



def test_admin_delete_todo_not_found(test_todo):
    response = client.delete('/admin/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}