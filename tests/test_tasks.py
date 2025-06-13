"""
Tests automatisés pour les routes liées aux tâches (tasks) dans l'API FastAPI.

Ce module utilise TestClient pour simuler des requêtes HTTP contre l'application.
Il couvre :
- L'authentification utilisateur et récupération du token JWT,
- La création d'une tâche avec authentification,
- La récupération de toutes les tâches,
- La récupération d'une tâche spécifique par son ID,
- La mise à jour d'une tâche.

Chaque test vérifie le code HTTP de la réponse et la cohérence des données retournées.
"""

from fastapi.testclient import TestClient
import sys
import os

# Ajouter le dossier parent au chemin pour importer 'main'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Création du client de test FastAPI
client = TestClient(app)

# Données de connexion pour authentification
login_data = {
    "username": "Ariri",
    "password": "1234"
}

# Authentification et récupération du token d'accès JWT
response_login = client.post("/auth/login", json=login_data)
assert response_login.status_code == 200

token = response_login.json()["access_token"]
auth_headers = {"Authorization": f"Bearer {token}"}

def test_create_task_authenticated():
    """
    Teste la création d'une tâche avec un utilisateur authentifié.

    Envoie une requête POST à /tasks/ avec un token valide,
    vérifie que la tâche est créée avec succès et que les données correspondent.
    """
    headers = auth_headers
    task_data = {
        "title": "Réviser FastAPI",
        "description": "Lire la doc",
        "status": "todo",
        "due_date": "2025-06-20T00:00:00Z",
        "owner_id": 1
    }

    response = client.post("/tasks/", json=task_data, headers=headers)
    print("Erreur:", response.status_code, response.json())  # Pour debug si besoin
    assert response.status_code in (200, 201)

    data = response.json()
    assert data["title"] == "Réviser FastAPI"
    assert data["status"] == "todo"

def test_get_all_tasks():
    """
    Teste la récupération de toutes les tâches avec authentification.

    Envoie une requête GET à /tasks/ et vérifie que la réponse est une liste.
    """
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_task_by_id():
    """
    Teste la récupération d'une tâche spécifique via son ID.

    Crée d'abord une tâche, puis récupère cette tâche via GET /tasks/{id}.
    Vérifie la correspondance de l'ID et du titre.
    """
    create_resp = client.post(
        "/tasks/",
        json={
            "title": "Tâche temporaire",
            "description": "Juste pour le test",
            "status": "todo",
            "due_date": "2025-06-20",
            "owner_id": 1
        },
        headers=auth_headers
    )
    task_id = create_resp.json()["id"]

    get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == task_id
    assert data["title"] == "Tâche temporaire"

def test_update_task():
    """
    Teste la mise à jour d'une tâche existante.

    Crée une tâche, la met à jour via PUT /tasks/{id},
    puis vérifie que les champs modifiés sont bien mis à jour.
    """
    create_resp = client.post(
        "/tasks/",
        json={
            "title": "Ancien titre",
            "description": "Ancienne description",
            "status": "todo",
            "due_date": "2025-06-21",
            "owner_id": 1
        },
        headers=auth_headers
    )
    task_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Nouveau titre",
            "description": "Description mise à jour",
            "status": "in_progress",
            "due_date": "2025-06-30",
            "owner_id": 1
        },
        headers=auth_headers
    )
    assert update_resp.status_code == 200
    updated_task = update_resp.json()
    assert updated_task["title"] == "Nouveau titre"
    assert updated_task["status"] == "in_progress"
 