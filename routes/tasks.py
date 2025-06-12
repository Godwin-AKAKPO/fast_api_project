# routes/tasks.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# --- Modèle Pydantic (pour valider les données entrantes) ---
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# --- Données simulées ---
tasks_db = []

# --- Routes CRUD ---
@router.get("/", response_model=List[Task])
def get_tasks():
    return tasks_db

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tâche non trouvée")

@router.post("/", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            tasks_db[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Tâche non trouvée")

@router.delete("/{task_id}")
def delete_task(task_id: int):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            tasks_db.pop(i)
            return {"message": "Tâche supprimée"}
    raise HTTPException(status_code=404, detail="Tâche non trouvée")
