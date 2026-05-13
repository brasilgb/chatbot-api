import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import test_connection

from app.modules.chat.router import router as chat_router
from app.modules.resumo_total.router import router as resumo_total_router


logging.basicConfig(
    level=logging.INFO if settings.app_env == "production" else logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(
    title="Grupo Solar Chatbot API",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Arquivos estáticos
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# Routers
app.include_router(chat_router)
app.include_router(resumo_total_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Chatbot API funcionando",
    }


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/health/db")
def health_db():
    return {
        "database": "connected" if test_connection() else "failed"
    }