Projet API REST avec Fast

## Prérequis

- Python et dépendances installées (`pip install -r requirements.txt`)
- Base de données configurée (MySQL, PostgreSQL, etc.)
- Alembic installé (`pip install alembic`)

## Configuration de la base de données

Les paramètres de connexion à la base de données sont définis dans un fichier `.env` à la racine du projet :

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=""
DB_PORT=3306
DB_NAME=tache_manage

## Execution des migrations

alembic upgrade head