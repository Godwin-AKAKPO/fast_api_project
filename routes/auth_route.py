from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin, Token
from database import get_db
from auth import (verify_password, get_password_hash, create_access_token, get_current_user)

router = APIRouter(tags=["Authentification"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # On verifie si l'utilisateur existe déjà
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)

    # On cree un nouvel utilisateur
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()

    # On genere un token d'accès
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # On cherche l'utilisateur
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code = 401, detail="Identifiants invalides")
    
    # On genere le token 
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
