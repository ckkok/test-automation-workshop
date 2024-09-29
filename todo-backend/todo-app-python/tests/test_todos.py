import pytest
from fastapi.testclient import TestClient
from app.main import app 
from app.database import get_db, get_test_db, Base, test_engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

app.dependency_overrides[get_db] = get_test_db

def test_create_todo():
    todo_data = {
        "task": "Test Todo",
        "completed": False
    }
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 200
    data = response.json()
    assert data["task"] == todo_data["task"]

def test_read_todos():
    todo_data = {
        "task": "Test Todo",
        "completed": False
    }
    client.post("/todos/", json=todo_data)

    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["task"] == todo_data["task"]
