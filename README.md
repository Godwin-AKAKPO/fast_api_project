# 🧩 FastAPI Task Manager API

Une API RESTful de gestion de tâches construite avec **FastAPI**, **SQLAlchemy** et **MySQL**, incluant un système d'authentification par JWT.


---


## 🚀 Fonctionnalités

- Authentification JWT (inscription, connexion)
- Gestion des utilisateurs
- Création, lecture, mise à jour et suppression de tâches (CRUD)
- Tests automatisés avec `pytest`
- Documentation interactive via Swagger UI


---


## 🗂️ Structure du projet

```bash
.
├── main.py # Point d'entrée de l'application
├── models.py # Modèles SQLAlchemy
├── database.py # Connexion et session DB
├── auth.py # Authentification et sécurité JWT
├── routes/
│   ├── auth_route.py # Routes d'authentification
│   ├── tasks.py # Routes des tâches
│   └── hello.py # Route de test /hello
├── tests/
│   ├── test_auth.py # Tests de l'authentification
│   └── test_tasks.py # Tests des tâches
├── requirements.txt # Dépendances Python
└── README.md # Documentation du projet
```


---


## Prérequis

- Python et dépendances installées (`pip install -r requirements.txt`)
- Base de données configurée (MySQL, PostgreSQL, etc.)
- Alembic installé (`pip install alembic`)


---


## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-nom/fastapi-task-manager.git
cd fastapi-task-manager
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # sous Windows : venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer du fichier `.env`

Créer un fichier .env à la racine du projet :

```ini
DB_USER=root
DB_PASSWORD=motdepasse
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ma_base
```

### 5. Exécuter les migrations

```bash
alembic upgrade head
```


---


## ▶️ Lancer l'application

```bash
uvicorn main:app --reload
```


---


## 📑 Accès à la documentation

- Swagger UI : http://127.0.0.1:8000/docs

- ReDoc : http://127.0.0.1:8000/redoc


---


## 🧪 Exécuter les tests

```bash
pytest
```


---


## 🧠 Notes techniques

- Le hashage des mots de passe est fait avec passlib (bcrypt)

- Les tokens sont générés avec jose/jwt

- Les schémas de validation sont gérés avec Pydantic

- Base de données relationnelle : MySQL



---


## 📌 Perspectives 

- Pagination & filtres

- Déploiement (Render, Docker...)


---


## 👨‍💻 Auteurs

Projet réalisé dans le cadre d'un projet de classe par :
- AGBOTON Ariane
- AKAKPO Godwin
- CODO Jean-Eudes
- KOFFI Angelina
- SOULEYMANE Hosny


## 📃 Licence
Ce projet est sous licence MIT.


