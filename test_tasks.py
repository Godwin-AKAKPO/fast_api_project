# test_tasks.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks/", json={
        "id": 1,
        "title": "Faire les courses",
        "description": "Acheter du pain et du lait",
        "completed": False
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Faire les courses"

def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    response = client.put("/tasks/1", json={
        "id": 1,
        "title": "Courses modifiées",
        "description": "Juste du lait",
        "completed": True
    })
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Tâche supprimée"
