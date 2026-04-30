from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    success: bool
    answer: str
    intent: dict | None = None