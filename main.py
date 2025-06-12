from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from routes import hello
from database import engine
from routes import tasks

app = FastAPI(title="API")


@app.get("/")
def read_root():
    return {"message": "Bonjour depuis votre API FastAPI"}

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Connexion OK")
    except Exception as e:
        print("Erreur de connexion :", e)

if __name__ == "__main__":
    test_connection()
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])



app.include_router(hello.router, prefix="/hello", tags=["hello"])
