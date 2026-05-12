from pydantic import BaseModel, Field
from typing import Any


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
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
