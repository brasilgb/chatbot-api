from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.modules.chat.service import processar_chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    history: Optional[List[Dict[str, Any]]] = None


@router.post("/")
def chat(request: ChatRequest):
    return processar_chat(
        message=request.message,
        session_id=request.session_id or "default",
    )
