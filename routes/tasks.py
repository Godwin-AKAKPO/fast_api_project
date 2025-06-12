# routes/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from models import Tache
from database import get_db
from datetime import datetime

router = APIRouter()

# ----- Schémas Pydantic -----
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    due_date: Optional[datetime] = None
    owner_id: int

class TaskResponse(TaskCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ----- Routes connectées à la base de données -----
@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Tache).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Tache).filter(Tache.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Tache(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Tache).filter(Tache.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    for key, value in updated_task.dict().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Tache).filter(Tache.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    db.delete(task)
    db.commit()
    return {"message": "Tâche supprimée"}
