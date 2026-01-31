from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    message = req.message.strip().lower()
    language = req.language or "en"

    print(f"📩 User said: {req.message} | Language: {language}")

    # ✅ Greeting handling (NO LLM)
    if message in ["hi", "hello", "hey", "namaste"]:
        return ChatResponse(
            mode="answer",
            intent="unknown",
            language=language,
            answer=(
                "Hello! 👋 I’m SahajAI.\n\n"
                "I can help you with:\n"
                "• Government schemes\n"
                "• Required documents\n"
                "• Office guidance (Tehsil, CSC, Jan Seva Kendra)\n"
                "• Step-by-step form filling\n\n"
                "How can I assist you today?"
            ),
            next_actions=[
                "Ask about a government scheme",
                "Ask which documents are required",
                "Ask where to apply for a service",
                "Ask for help filling a form"
            ],
            confidence=0.9
        )

    # fallback placeholder (temporary)
    return ChatResponse(
        mode="answer",
        intent="unknown",
        language=language,
        answer=f"You said: {req.message}. SahajAI will process this.",
        confidence=0.2
    )
