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

# ----- Routes CRUD pour les tâches -----

@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    """
    Récupère toutes les tâches.

    Args:
        db (Session): Session de base de données.

    Returns:
        List[TaskResponse]: Liste des tâches existantes.
    """
    return db.query(Tache).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Récupère une tâche par son identifiant.

    Args:
        task_id (int): ID de la tâche à récupérer.
        db (Session): Session de base de données.

    Raises:
        HTTPException 404: Si la tâche n'existe pas.

    Returns:
        TaskResponse: La tâche trouvée.
    """
    task = db.query(Tache).filter(Tache.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle tâche.

    Args:
        task (TaskCreate): Données de la tâche à créer.
        db (Session): Session de base de données.

    Returns:
        TaskResponse: La tâche créée.
    """
    db_task = Tache(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    """
    Met à jour une tâche existante.

    Args:
        task_id (int): ID de la tâche à modifier.
        updated_task (TaskCreate): Données mises à jour.
        db (Session): Session de base de données.

    Raises:
        HTTPException 404: Si la tâche n'existe pas.

    Returns:
        TaskResponse: La tâche mise à jour.
    """
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
    """
    Supprime une tâche par son identifiant.

    Args:
        task_id (int): ID de la tâche à supprimer.
        db (Session): Session de base de données.

    Raises:
        HTTPException 404: Si la tâche n'existe pas.

    Returns:
        dict: Message de confirmation.
    """
    task = db.query(Tache).filter(Tache.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    db.delete(task)
    db.commit()
    return {"message": "Tâche supprimée"}
