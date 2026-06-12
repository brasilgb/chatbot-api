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
    session_id: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = None


class ChatResponse(BaseModel):
    success: bool
    type: Optional[str] = "text"
    answer: str
    intent: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    image_path: Optional[str] = None
    requires_selection: Optional[bool] = None
    selection_type: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return processar_chat(message=request.message, session_id=request.session_id)
