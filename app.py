from flask import Flask
from flask_restx import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv  # <- importer load_dotenv
from sqlalchemy import text

# Charger les variables du fichier .env dans l'environnement
load_dotenv()

app = Flask(__name__)
api = Api(app, title='API')

ns = api.namespace('hello', description='Hello operations')

@ns.route('/')
class HelloResource(Resource):
    def get(self):
        """Retourne un message de bienvenue"""
        return {'message': 'Bonjour depuis votre API Flask'}

# Construire la chaîne de connexion à partir des variables d'environnement
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Connexion OK")
    except Exception as e:
        print("Erreur de connexion :", e)

if __name__ == '__main__':
    test_connection()
    app.run(debug=True)
