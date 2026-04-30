from fastapi import FastAPI

from app.core.database import test_connection
from app.modules.lojas.faturamento.router import router as faturamento_router
from app.modules.chat.router import router as chat_router

app = FastAPI(title="Grupo Solar Chatbot API", version="1.0.0")

# routers
app.include_router(faturamento_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"status": "online", "message": "Chatbot API funcionando"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/health/db")
def health_db():
    return {"database": "connected" if test_connection() else "failed"}
