from fastapi import FastAPI

from app.core.database import test_connection

app = FastAPI(
    title="Grupo Solar Chatbot API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Chatbot API funcionando"
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/health/db")
def health_db():
    return {
        "database": "connected" if test_connection() else "failed"
    }