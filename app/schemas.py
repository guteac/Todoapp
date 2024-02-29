from pydantic import BaseModel, Field

class SendTodo(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=5, max_length=150)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    class Config():
        json_schema_extra = {
            'example': {
                'title': 'A new to do',
                'description': 'this to do is very important because...',
                'priority': 4,
                'complete': False
            }
        }

class SendUser(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=30)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=5, max_length=30)
    is_active: bool
    role: str = Field(min_length=3, max_length=10)

    class Config():
        json_schema_extra = {
            'example': {
                'email': 'john@email.com',
                'username': 'johndoe',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'password123',
                'is_active': True,
                'role': 'admin'
            }
        }

class LoginResponse(BaseModel):
    token: str
    token_type: str

    class ConfigDict:
        orm_mode = True

class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)