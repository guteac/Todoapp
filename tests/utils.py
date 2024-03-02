from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import Base
from sqlalchemy.pool import StaticPool
from app.models import Todos, Users
from app.main import app
from app.utils import get_password_hash, verify_credentials
from fastapi.testclient import TestClient
import pytest


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'john@email.com', 'user_id': 1, 'user_role': 'admin'}#these are the informations that get_db returns normally -> It decodes the JWT token and returns these informations for each API that requires it(that call get_db)(see oauth2.py).

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title = 'To water the plants',
        description = 'I need to water the plants everyday',
        priority = 4,
        complete = False,
        owner_id = 1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo #after the test finishes for each endpoint
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username = 'johndoe',
        email = 'john@email.com',
        first_name = 'john',
        last_name = 'Doe',
        password = get_password_hash('password123'),
        role = 'admin',
        phone_number = '(111)-111-1111'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user #after the test finishes for each endpoint
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()


@pytest.fixture
def test_todo_admin():
    todo = Todos(
        title = 'Go to the gym',
        description = 'I need to go to the gym three time a week!',
        priority = 4,
        complete = False,
        owner_id = 2
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo #after the test finishes for each endpoint
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()