from fastapi import FastAPI
from .database import engine
from .routers import todos, users, login, admin
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/healthy')
async def health_check():
    return {'status': 'Healthy'}

app.include_router(todos.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(admin.router)

@app.get('/')
async def welcome_page():
    return {'message': 'Hello and Welcome!'}