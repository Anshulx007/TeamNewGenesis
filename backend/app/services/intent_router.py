def detect_intent(message: str) -> str:
    text = message.lower()

    if any(k in text for k in ["scheme", "yojana", "pm", "ration"]):
        return "scheme_info"

    if any(k in text for k in ["document", "documents", "required", "aadhaar", "income"]):
        return "document_help"

    if any(k in text for k in ["office", "where", "tehsil", "csc"]):
        return "office_locator"

    return "unknown"
def split_questions(message: str):
    # split by question words or punctuation
    separators = ["?", " what ", " where ", " how "]
    questions = [message]

    for sep in separators:
        new = []
        for q in questions:
            new.extend(q.split(sep))
        questions = new

    return [q.strip() for q in questions if len(q.strip()) > 5]
