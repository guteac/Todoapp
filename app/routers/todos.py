from fastapi import Depends, status, HTTPException, APIRouter, Path
from sqlalchemy.orm import Session
from ..models import Todos
from ..database import get_db
from ..schemas import SendTodo
from ..oauth2 import get_current_user
from sqlalchemy import func



router = APIRouter(
    tags = ['Todos']
)

@router.get('/todo', status_code=status.HTTP_200_OK)
async def get_all(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()
    return query



@router.get('/todo/{id}', status_code=status.HTTP_200_OK)
async def get_by_id(id: int = Path(gt=0), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Todos).filter(Todos.id == id).filter(Todos.owner_id == user.get('user_id')).first()
    if query is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    return query



@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(todo: SendTodo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo_to_post = Todos(**todo.model_dump(), owner_id=user.get('user_id'))#transform the request body into a Todo Object(open the JSON 'dictionary' and transform in an object of todo class)
    db.add(todo_to_post)
    db.commit()



@router.put('/todo/{id}', status_code=status.HTTP_202_ACCEPTED)
async def edit_todo(todo: SendTodo, id: int = Path(gt=0), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):#ppydantic model before id(Path parameters)
    query = db.query(Todos).filter(Todos.id == id).filter(Todos.owner_id == user.get('user_id'))
    todo_to_edit = query.first()#update and delete have to be like this

    if todo_to_edit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    
    query.update(todo.model_dump(), synchronize_session=False)
    db.commit()



@router.delete('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int = Path(gt=0), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Todos).filter(Todos.id == id).filter(Todos.owner_id == user.get('user_id'))
    todo_to_delete = query.first()#update and delete have to be like this

    if todo_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    
    query.delete(synchronize_session=False)
    db.commit()