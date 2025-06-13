from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def say_hello():
    """
    Endpoint simple qui retourne un message de bienvenue.
    
    Returns:
        dict: Message de bienvenue.
    """
    return {"message": "Bonjour depuis l'endpoint /hello"}
