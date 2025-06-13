"""
Gère l'authentification, la génération de tokens JWT et la vérification des utilisateurs.

Ce module fournit les fonctions pour :
- Vérifier les mots de passe,
- Hacher les mots de passe,
- Créer des tokens JWT,
- Extraire l'utilisateur courant à partir d'un token d'accès.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db
from models import User

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe en clair correspond au mot de passe haché.

    Args:
        plain_password (str): Le mot de passe en clair fourni par l'utilisateur.
        hashed_password (str): Le mot de passe stocké haché en base.

    Returns:
        bool: True si le mot de passe correspond, False sinon.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Génère le hash sécurisé d'un mot de passe.

    Args:
        password (str): Le mot de passe en clair.

    Returns:
        str: Le mot de passe haché.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """
    Crée un token JWT d'accès avec une durée d'expiration.

    Args:
        data (dict): Données à encoder dans le token (ex: {'sub': username}).

    Returns:
        str: Token JWT encodé.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Récupère l'utilisateur courant à partir du token JWT.

    Args:
        token (str): Token JWT extrait via OAuth2.
        db (Session): Session SQLAlchemy pour la base de données.

    Raises:
        HTTPException: Erreur 401 si le token est invalide, expiré ou si l'utilisateur n'existe pas.

    Returns:
        User: Objet utilisateur correspondant au token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expiré ou invalide")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur non trouvé")
    return user
