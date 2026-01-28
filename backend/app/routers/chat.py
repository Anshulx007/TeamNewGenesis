from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    language: str | None = "en"

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # TEMP: Demo reply (LLM comes next)
    reply = f"You said: {req.message}. SahajAI will process this."

    return ChatResponse(reply=reply)
