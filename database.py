"""
Gère la connexion à la base de données MySQL et l'initialisation des tables via SQLAlchemy.

Ce module :
- Charge les variables d'environnement,
- Crée l'engine SQLAlchemy,
- Définit la session locale pour la gestion des transactions,
- Fournit une base pour les modèles ORM,
- Offre une fonction utilitaire pour obtenir une session DB.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os

# Charger les variables d’environnement depuis .env
load_dotenv()

# Variables d'environnement pour la connexion à la base de données
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Construction de l'URL de connexion MySQL avec le driver pymysql
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Création du moteur SQLAlchemy (connexion à la base)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création d'une session locale pour les transactions avec la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour définir les modèles ORM
Base = declarative_base()

def get_db():
    """
    Fournit une session de base de données SQLAlchemy à utiliser dans les routes.

    Cette fonction est un générateur qui ouvre une session et la ferme proprement après utilisation.

    Yields:
        Session: Une session active SQLAlchemy liée à la base de données.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
