from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..models import Users
from ..database import get_db
from ..schemas import SendUser, ChangePassword
from ..utils import get_password_hash, verify_credentials
from ..oauth2 import get_current_user



router = APIRouter(
    tags = ['Users']
)

@router.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(user: SendUser,db: Session = Depends(get_db)):

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = Users(**user.model_dump())#transform from JSON to Users object
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/user/my_user', status_code=status.HTTP_200_OK)
async def my_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Users).filter(Users.email == user.get('username')).first()

@router.put('/user/password', status_code=status.HTTP_200_OK)
async def change_password(passwords: ChangePassword, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Users).filter(Users.email == user.get('username')).first()
    if verify_credentials(passwords.current_password, query.password) != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')
    query.password = get_password_hash(passwords.new_password)

    db.add(query)
    db.commit()
