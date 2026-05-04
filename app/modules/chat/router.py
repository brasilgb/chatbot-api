from fastapi import APIRouter
from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.service import process_chat

from pydantic import BaseModel
from app.modules.chat.aprendizado_service import (
    salvar_aprendizado,
    get_aprendizados,
)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    return await process_chat(payload.message)

class AprendizadoRequest(BaseModel):
    pergunta_original: str
    pergunta_chave: str
    resposta: str
    intent: dict | None = None


@router.post("/dashboard/aprendizados")
def criar_aprendizado_endpoint(payload: AprendizadoRequest):
    data = salvar_aprendizado(
        pergunta_original=payload.pergunta_original,
        pergunta_chave=payload.pergunta_chave,
        resposta=payload.resposta,
        intent=payload.intent,
    )

    return {
        "success": True,
        "data": data,
    }


@router.get("/dashboard/aprendizados")
def listar_aprendizados_endpoint(limit: int = 50):
    return {
        "success": True,
        "data": get_aprendizados(limit=limit),
    }