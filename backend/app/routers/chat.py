from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.intent_router import detect_intent, split_questions
from app.services.knowledge_service import get_document_info, get_scheme_info

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    message = req.message.strip().lower()
    language = req.language or "en"

    # -------------------------
    # GREETING (NO LLM)
    # -------------------------
    if message in ["hi", "hello", "hey", "namaste", "नमस्ते"]:
        if language == "hi":
            return ChatResponse(
                mode="answer",
                intent="unknown",
                language="hi",
                answer=(
                    "नमस्ते! 👋 मैं SahajAI हूँ।\n\n"
                    "मैं आपकी मदद कर सकता हूँ:\n"
                    "• सरकारी योजनाओं की जानकारी\n"
                    "• आवश्यक दस्तावेज़\n"
                    "• कार्यालय मार्गदर्शन (तहसील, CSC, जन सेवा केंद्र)\n"
                    "• फ़ॉर्म भरने के चरण\n\n"
                    "आप क्या जानना चाहते हैं?"
                ),
                confidence=0.9
            )

        return ChatResponse(
            mode="answer",
            intent="unknown",
            language="en",
            answer=(
                "Hello! 👋 I’m SahajAI.\n\n"
                "I can help you with:\n"
                "• Government schemes\n"
                "• Required documents\n"
                "• Office guidance (Tehsil, CSC, Jan Seva Kendra)\n"
                "• Step-by-step form filling\n\n"
                "How can I assist you today?"
            ),
            confidence=0.9
        )

    # -------------------------
    # MULTI-QUESTION HANDLING
    # -------------------------
    questions = split_questions(message)
    answers = set()  # 🔑 use set to avoid duplicates

    for q in questions:
        intent = detect_intent(q)

        if intent == "document_help":
            key, data = get_document_info(q)
            if data:
                answers.add(
                    f"Documents required for {key.title()}:\n" +
                    "\n".join(f"- {d}" for d in data["documents"])
                )

        elif intent == "scheme_info":
            key, data = get_scheme_info(q)
            if data:
                answers.add(data["description"])

    # ✅ RETURN COMBINED ANSWER
    if answers:
        return ChatResponse(
            mode="answer",
            intent="multi",
            language=language,
            answer="\n\n".join(sorted(answers)),
            confidence=0.8
        )

    # -------------------------
    # FINAL FALLBACK (BILINGUAL)
    # -------------------------
    if language == "hi":
        return ChatResponse(
            mode="fallback",
            intent="unknown",
            language="hi",
            answer=(
                "माफ़ कीजिए, मुझे इस प्रश्न की सटीक जानकारी नहीं मिली।\n"
                "कृपया सरकारी योजनाओं, दस्तावेज़ों या कार्यालयों से संबंधित प्रश्न पूछें।"
            ),
            confidence=0.3
        )

    return ChatResponse(
        mode="fallback",
        intent="unknown",
        language="en",
        answer=(
            "Sorry, I couldn’t find exact information for this query.\n"
            "Please ask about government schemes, documents, or offices."
        ),
        confidence=0.3
    )
