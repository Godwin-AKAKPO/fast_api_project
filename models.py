"""
Définit les modèles de données utilisés par l'application avec SQLAlchemy ORM.

Contient les classes User et Tache représentant respectivement les utilisateurs
et leurs tâches associées dans la base de données.
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    """
    Modèle représentant un utilisateur dans la base de données.

    Attributs :
        id (int) : Identifiant unique de l'utilisateur.
        username (str) : Nom d'utilisateur unique.
        email (str) : Adresse email unique.
        hashed_password (str) : Mot de passe haché.
        is_active (bool) : Statut actif/inactif de l'utilisateur.
        tasks (list[Tache]) : Liste des tâches associées à l'utilisateur.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Tache", back_populates="owner")


class Tache(Base):
    """
    Modèle représentant une tâche dans la base de données.

    Attributs :
        id (int) : Identifiant unique de la tâche.
        title (str) : Titre de la tâche.
        description (str) : Description détaillée de la tâche.
        status (str) : Statut de la tâche ("todo", "in_progress", "done").
        created_at (datetime) : Date et heure de création de la tâche.
        due_date (datetime) : Date limite pour la tâche.
        owner_id (int) : Identifiant de l'utilisateur propriétaire.
        owner (User) : Relation vers l'utilisateur propriétaire.
    """

    __tablename__ = "taches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="todo")  # valeurs possibles : todo, in_progress, done
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
