from datetime import timedelta
from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import Users
from ..utils import verify_credentials
from ..oauth2 import create_access_token
from ..schemas import LoginResponse

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user  = db.query(Users).filter(Users.email == credentials.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if verify_credentials(credentials.password, user.password) != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    token = create_access_token(user.email, user.id, user.role, timedelta(minutes=20))
    
    return {'token': token, 'token_type': 'bearer'}