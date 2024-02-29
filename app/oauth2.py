from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

def create_access_token(username: str, user_id: int, user_role: str, expires_delta: timedelta):
    to_encode = {'user': username, 'id': user_id, 'role': user_role}
    expires = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expires})
    
    return jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")#passing the login page as reference(dependency that each api endpoint will rely on)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        username: str = payload.get('user')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        
        return {'username': username, 'user_id': user_id, 'user_role': user_role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')