# routers/hello.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def say_hello():
    return {"message": "Bonjour depuis l'endpoint /hello"}
