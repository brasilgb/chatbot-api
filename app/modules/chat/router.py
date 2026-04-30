from fastapi import APIRouter
from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.service import process_chat

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    return await process_chat(payload.message)