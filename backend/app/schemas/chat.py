from pydantic import BaseModel
from typing import List, Literal

class ChatRequest(BaseModel):
    message: str
    language: str | None = "en"

class ChatResponse(BaseModel):
    mode: Literal["answer", "fallback", "error"]
    intent: str
    language: str
    answer: str
    steps: List[str] = []
    references: List[str] = []
    next_actions: List[str] = []
    confidence: float = 0.0
