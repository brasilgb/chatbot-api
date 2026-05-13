from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.chat.service import processar_chat


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(request: ChatRequest):
    return processar_chat(request.message)