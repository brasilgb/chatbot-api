from pydantic import BaseModel
from typing import Any


class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, Any]] | None = None
    date: str | None = None


class ChatResponse(BaseModel):
    success: bool
    answer: str | None = None
    reply: str | None = None
    intent: dict[str, Any] | None = None
    source: str | None = None
    error: str | None = None
    image_path: str | None = None