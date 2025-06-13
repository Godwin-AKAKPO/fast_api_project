"""
Tests automatisés pour les routes d'authentification de l'API FastAPI.

Ce module teste les fonctionnalités d'inscription (register) et de connexion (login),
notamment :
- Inscription d'un nouvel utilisateur avec des données valides,
- Gestion d'une tentative d'inscription avec un nom d'utilisateur déjà pris,
- Connexion réussie avec des identifiants valides,
- Échec de connexion avec un mot de passe incorrect,
- Échec de connexion avec un utilisateur inexistant.
"""

from fastapi.testclient import TestClient
import sys
import os
import uuid

# Permet d'importer main.py qui est un niveau au-dessus du dossier tests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_register_user():
    """
    Teste l'inscription d'un nouvel utilisateur avec des données valides.

    Vérifie que la réponse contient un token d'accès et que le code HTTP est 200 ou 201.
    """
    user_data = {
        "username": f"testuser_{uuid.uuid4().hex[:8]}",
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
        "password": "testpassword123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_existing_user():
    """
    Teste la tentative d'inscription avec un nom d'utilisateur déjà pris.

    La première inscription devrait réussir,
    la deuxième tenter d'inscrire le même utilisateur devrait échouer
    avec un code HTTP 400 ou 409 (conflit).
    """
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    # Première inscription (success)
    client.post("/auth/register", json=user_data)
    # Deuxième tentative (devrait échouer)
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400 or response.status_code == 409

def test_login_user():
    """
    Teste la connexion avec des identifiants valides.

    Inscrit d'abord un utilisateur, puis vérifie que la connexion
    retourne un token d'accès avec un code HTTP 200.
    """
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    client.post("/auth/register", json=user_data)

    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """
    Teste la tentative de connexion avec un mauvais mot de passe.

    L'utilisateur est inscrit avec un mot de passe correct,
    puis une connexion est tentée avec un mot de passe incorrect,
    ce qui doit renvoyer un code HTTP 401.
    """
    user_data = {
        "username": "loginuser2",
        "password": "correctpassword"
    }
    client.post("/auth/register", json=user_data)

    wrong_login = {
        "username": "loginuser2",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=wrong_login)
    assert response.status_code == 401

def test_login_nonexistent_user():
    """
    Teste la connexion avec un utilisateur qui n'existe pas.

    La tentative doit échouer avec un code HTTP 401.
    """
    user_data = {
        "username": "userdoesnotexist",
        "password": "whatever"
    }
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 401
