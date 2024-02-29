from fastapi import status, HTTPException, APIRouter, Depends, Path
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import Todos
from ..oauth2 import get_current_user

router = APIRouter(
    tags = ['Administration']
)

@router.get('/admin/todo', status_code=status.HTTP_200_OK)
async def get_all_todos(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return db.query(Todos).all()

@router.delete('/admin/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int = Path(gt=0), user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    query = db.query(Todos).filter(Todos.id == id)
    todo_to_delete = query.first()
    if todo_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    
    query.delete(synchronize_session=False)
    db.commit()