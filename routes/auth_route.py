from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin, Token
from database import get_db
from auth import verify_password, get_password_hash, create_access_token

router = APIRouter(tags=["Authentification"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Route d'inscription d'un nouvel utilisateur.

    - Vérifie si le nom d'utilisateur existe déjà en base.
    - Hash le mot de passe.
    - Crée un nouvel utilisateur dans la base.
    - Génère un token d'accès JWT et le retourne.

    Args:
        user (UserCreate): Données d'inscription de l'utilisateur.
        db (Session): Session de base de données injectée.

    Raises:
        HTTPException: Si le nom d'utilisateur est déjà pris (code 400).

    Returns:
        dict: Token JWT avec type "bearer".
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Pour rafraîchir l'objet avec l'ID généré

    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Route de connexion utilisateur.

    - Recherche l'utilisateur en base par nom d'utilisateur.
    - Vérifie que le mot de passe correspond.
    - Génère un token d'accès JWT et le retourne.

    Args:
        user (UserLogin): Données de connexion (username, password).
        db (Session): Session de base de données injectée.

    Raises:
        HTTPException: Si utilisateur non trouvé ou mot de passe invalide (code 401).

    Returns:
        dict: Token JWT avec type "bearer".
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
